# Knowledge Base for CyberBot Assistant

INTENTS = {
    "GREETING": {
        "patterns": ["hello", "hi", "hey", "greetings", "yo"],
        "responses": ["Hello! I'm CyberBot, your symposium assistant. How can I help you sparkle today? ✨", "Hi there! Ready to explore CyberNova 2026? 🚀"]
    },
    "EVENTS": {
        "patterns": ["event", "list events", "what are the events", "available events", "activities", "competitions"],
        "responses": [
            "At CyberNova 2026, we have 10 premier events: Open Source Hackathon, Paper Presentation, Web Dev Challenge, AI & ML Ideathon, UI/UX Design Sprint, Git Bootcamp, Coding Marathon, Startup Pitch, Tech Quiz, and OS Contribution Drive! \n\nWould you like details or prize info for any specific event?"
        ]
    },
    "REGISTRATION": {
        "patterns": ["register", "signup", "sign up", "join", "apply"],
        "responses": ["You can register via the 'Register Now' button in the navbar. You'll need your registration number and to pick an event!", "Sign up is quick! Just hit 'Register Now' on the header. Which event are you interested in?"]
    },
    "PRIZES": {
        "patterns": ["prize", "award", "win", "reward", "money"],
        "responses": ["Platinum winners get ₹10,000 + Tech Kits. Gold and Silver tiers also have great cash awards and internship offers! 🏆", "We have prizes worth over ₹50,000 in total! Would you like to know about the internship opportunities too?"]
    },
    "SCHEDULE": {
        "patterns": ["schedule", "time", "when", "start", "duration"],
        "responses": ["We start at 9:00 AM with the inauguration. You can see the full timeline on the 'Updates' page! 📅", "Most events kick off at 10:30 AM. Check the 'Updates' section for the live schedule."]
    },
    "VENUE": {
        "patterns": ["venue", "location", "where", "place", "room", "lab"],
        "responses": ["The main events are in the Auditorium. Technical events are in the CSE Department labs. 📍", "Check the signage on campus! CSE Department is the hub for all CyberNova sessions."]
    },
    "RECOMMENDATION_START": {
        "patterns": ["recommend", "suggest", "help me choose", "best event", "what should i do"],
        "responses": ["I'd love to suggest an event! What are you into? AI, Web Dev, UI/UX, or Research? 🤖"]
    },
    "WHO_AM_I": {
        "patterns": ["who are you", "what are you", "your name"],
        "responses": ["I am CyberBot, the digital soul of CyberNova 2026. I'm here to make your symposium experience seamless! 💻"]
    }
}

EVENT_INTERESTS = {
    "ai": ["AI & ML Ideathon", "Coding Marathon"],
    "ml": ["AI & ML Ideathon", "Coding Marathon"],
    "web": ["Web Dev Challenge", "Open Source Hackathon"],
    "design": ["UI/UX Design Sprint"],
    "ux": ["UI/UX Design Sprint"],
    "research": ["Paper Presentation"],
    "paper": ["Paper Presentation"],
    "code": ["Open Source Hackathon", "Coding Marathon", "Git & GitHub Bootcamp"]
}

FALLBACK_RESPONSE = "I'm not exactly sure about that, but I'm learning! You can ask about events, prizes, registration, or for a recommendation! 🚀"
