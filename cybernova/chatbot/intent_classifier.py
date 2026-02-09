import re
from .knowledge_base import INTENTS

class IntentClassifier:
    @staticmethod
    def classify(message):
        # Sanitize input: lowercase and strip whitespace
        message = message.lower().strip()
        
        # Check patterns for each intent
        for intent, data in INTENTS.items():
            for pattern in data["patterns"]:
                # Use word boundaries for single words, but allow phrase matching
                if re.search(r'\b' + re.escape(pattern) + r'\b', message) or pattern in message:
                    return intent
        
        return "UNKNOWN"
