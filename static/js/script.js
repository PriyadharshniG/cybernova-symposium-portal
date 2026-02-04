document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
    if (!form) return;

    const fields = {
        'full_name': { required: true, minLength: 3, msg: 'Name must be at least 3 chars' },
        'register_number': { required: true, pattern: /^[a-zA-Z0-9]+$/, msg: 'Alphanumeric characters only' },
        'department': { required: true, msg: 'Please select a department' },
        'year': { required: true, type: 'radio', msg: 'Please select your year' }, // Handling for radio handled separately
        'college_name': { required: true, minLength: 2, msg: 'Please enter valid college name' },
        'event': { required: true, msg: 'Please select an event' },
        'email': { required: true, pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, msg: 'Invalid email address' },
        'phone': { required: true, pattern: /^[0-9]{10}$/, msg: '10 digit phone number required' }
    };

    form.addEventListener('submit', (e) => {
        let valid = true;

        for (const [id, rules] of Object.entries(fields)) {
            let input;
            let errorSpan;

            if (rules.type === 'radio') {
                // Radio buttons share a name, not an id for the group usually
                const radios = document.getElementsByName(id);
                errorSpan = document.getElementById(`error-${id}`);
                const checked = Array.from(radios).some(r => r.checked);

                if (!checked) {
                    showError(errorSpan, rules.msg);
                    valid = false;
                } else {
                    clearError(errorSpan);
                }
                continue;
            }

            input = document.getElementById(id);
            if (!input) continue;

            errorSpan = document.getElementById(`error-${id}`);

            const value = input.value.trim();

            if (rules.required && !value) {
                showError(errorSpan, rules.msg || 'This field is required');
                valid = false;
            } else if (rules.minLength && value.length < rules.minLength) {
                showError(errorSpan, rules.msg);
                valid = false;
            } else if (rules.pattern && !rules.pattern.test(value)) {
                showError(errorSpan, rules.msg);
                valid = false;
            } else {
                clearError(errorSpan);
            }
        }

        if (!valid) {
            e.preventDefault();
            // Shake effect or scroll to top?
            // form.scrollIntoView({ behavior: 'smooth' });
        }
    });

    // Real-time validation (optional, can be noisy)
    /*
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            // clear error on input
            const id = input.id || input.name;
            const errorSpan = document.getElementById(`error-${id}`);
            if (errorSpan) clearError(errorSpan);
        });
    });
    */


    // --- Animation & Interaction Scripts ---

    // Scroll Reveal Interaction
    const revealElements = document.querySelectorAll('.glass-panel, h2, #events .glass-panel');
    revealElements.forEach(el => el.classList.add('reveal'));

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                // Optional: Stop observing once revealed
                // revealObserver.unobserve(entry.target); 
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    });

    revealElements.forEach(el => revealObserver.observe(el));

    // Navbar Scroll Effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Staggered Animations for Grids
    const grids = document.querySelectorAll('.glass-panel');
    // This simple selector gets all panels, let's refine to grids if possible or just use index
    // A better approach for specific grids:
    const eventCards = document.querySelectorAll('#events .glass-panel');
    eventCards.forEach((card, index) => {
        card.style.transitionDelay = `${(index % 3) * 100}ms`;
    });

    const themeCards = document.querySelectorAll('#themes .glass-panel');
    themeCards.forEach((card, index) => {
        card.style.transitionDelay = `${index * 150}ms`;
    });

    const organizerCards = document.querySelectorAll('#organizers .glass-panel');
    organizerCards.forEach((card, index) => {
        card.style.transitionDelay = `${index * 200}ms`;
    });

}); // End of DOMContentLoaded

if (span) {
    span.textContent = message;
    span.style.opacity = '1';
}
}

function clearError(span) {
    if (span) {
        span.textContent = '';
        span.style.opacity = '0';
    }
}
