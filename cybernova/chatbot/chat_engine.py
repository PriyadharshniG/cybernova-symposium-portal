from flask import session
import random
from .intent_classifier import IntentClassifier
from .knowledge_base import INTENTS, EVENT_INTERESTS, FALLBACK_RESPONSE

class ChatEngine:
    def __init__(self):
        self.classifier = IntentClassifier()

    def get_response(self, user_message):
        user_message = user_message.lower().strip()
        intent = self.classifier.classify(user_message)
        
        # Load context from session
        context = session.get('chat_context')
        
        # Logic for Recommendation Flow
        if context == "RECOMMENDATION_START":
            for interest, events in EVENT_INTERESTS.items():
                if interest in user_message:
                    session['chat_context'] = None # Clear context
                    events_list = ", ".join(events)
                    return f"Based on your interest in {interest.upper()}, I highly recommend: {events_list}! Would you like to register for one of these?"
            
            return "That sounds cool! However, I'm best at recommending for: AI, Web, Design, Code or Research. Which do you prefer?"

        # Handle Intent
        if intent != "UNKNOWN":
            session['chat_context'] = intent # Set new context
            return random.choice(INTENTS[intent]["responses"])
        
        # Handle follow-up questions for existing context
        if context:
            if any(word in user_message for word in ["more", "detail", "else", "tell me"]):
                if context == "PRIZES":
                    return "Apart from cash, winners get exclusive access to our partner networking event and a chance for direct internship interviews! 💼"
                if context == "REGISTRATION":
                    return "Once registered, you'll get a Digital ID pass in your portal. Make sure to download it for QR check-in! 🎫"

        # Fallback
        session['chat_context'] = None
        return FALLBACK_RESPONSE
