import unittest
import sys
import os
from flask import session

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Registration

class SymposiumTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_index_redirect(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(b'/register' in response.data)

    def test_register_page_loads(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Symposium Registration', response.data)

    def test_registration_submission(self):
        response = self.app.post('/register', data=dict(
            full_name='Test Student',
            register_number='12345',
            department='CSE',
            year='3rd',
            college_name='Test College',
            event='Coding',
            email='test@example.com',
            phone='1234567890'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration Successful', response.data)
        
        # Verify DB
        reg = Registration.query.first()
        self.assertIsNotNone(reg)
        self.assertEqual(reg.full_name, 'Test Student')

    def test_admin_access_unauthorized(self):
        response = self.app.get('/admin', follow_redirects=True)
        self.assertIn(b'Admin Login', response.data)

    def test_admin_login_and_view(self):
        # 1. Login
        login = self.app.post('/admin/login', data=dict(
            password='admin123'
        ), follow_redirects=True)
        self.assertIn(b'Admin Dashboard', login.data)
        
        # 2. Add a registration
        reg = Registration(
            full_name='Admin View Test',
            register_number='999',
            department='IT',
            year='4th',
            college_name='Admin College',
            event='Gaming',
            email='adminview@test.com',
            phone='9999999999'
        )
        db.session.add(reg)
        db.session.commit()
        
        # 3. Check dashboard data
        dashboard = self.app.get('/admin')
        self.assertIn(b'Admin View Test', dashboard.data)

    def test_csv_export(self):
        # Login first
        with self.app as c:
            with c.session_transaction() as sess:
                sess['logged_in'] = True
            
            # Create data
            reg = Registration(
                full_name='CSV Candidate',
                register_number='CSV001',
                department='MECH',
                year='2nd',
                college_name='CSV University',
                event='Quiz',
                email='csv@test.com',
                phone='8888888888'
            )
            db.session.add(reg)
            db.session.commit()
            
            response = c.get('/download_csv')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'text/csv')
            self.assertIn(b'CSV Candidate', response.data)

if __name__ == '__main__':
    unittest.main()
