from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob
import random

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/AI_Mental_Health_Chatbot_DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))
    account_type_id = db.Column(db.Integer, db.ForeignKey('account_type.account_type_id'))

class ChatSession(db.Model):
    __tablename__ = 'chat_session'
    session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    chat_log = db.Column(db.Text)

class EmotionTracking(db.Model):
    __tablename__ = 'emotion_tracking'
    emotion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.session_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    mood = db.Column(db.String(50))
    mood_score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

# Greeting Keywords and Responses
GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "what's up", "howdy"]
GREETING_RESPONSES = [
    "Hello there!",
    "Hi! How are you doing?",
    "Hey! How’s your day going?",
    "Greetings! What’s on your mind?",
    "Hello! How can I assist you today?",
    "Hey there! What’s happening?",
    "Hi! Let’s talk.",
    "Hello! How are you feeling today?",
    "Hi! What’s up?",
    "Hey! Ready to chat?"
]

# Conversation Trigger Keywords and Responses
CONVERSATION_KEYWORDS = ["can we talk", "let's talk", "want to talk", "need to talk", "talk to me"]
CONVERSATION_RESPONSES = [
    "Of course! What's on your mind?",
    "I'm here to listen. Please share your thoughts.",
    "Yes, let's talk. How can I support you?",
    "I'm ready to talk. What do you want to discuss?",
    "Sure, I'm here for you. What's bothering you?",
    "Let's have a chat. Tell me more.",
    "Absolutely! I'm here to help you. Go ahead.",
    "Yes, I'm all ears. Share what you're thinking.",
    "Let's talk. What's been going on?",
    "I'm here for you. Start whenever you're ready."
]

# Resources
RESOURCES = [
    {"title": "FindTreatment.gov", "link": "https://findtreatment.gov"},
    {"title": "Mental Health America", "link": "https://www.mhanational.org/"},
    {"title": "National Suicide Prevention Lifeline", "link": "https://suicidepreventionlifeline.org/"},
    {"title": "Crisis Text Line", "link": "https://www.crisistextline.org/"},
    {"title": "BetterHelp Online Therapy", "link": "https://www.betterhelp.com/"},
    {"title": "Psychology Today - Find a Therapist", "link": "https://www.psychologytoday.com/us/therapists"},
    {"title": "Substance Abuse and Mental Health Services Administration (SAMHSA)", "link": "https://www.samhsa.gov/"},
    {"title": "Anxiety and Depression Association of America", "link": "https://adaa.org/"},
    {"title": "National Institute of Mental Health", "link": "https://www.nimh.nih.gov/"},
    {"title": "The Trevor Project", "link": "https://www.thetrevorproject.org/"},
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    account_type_id = data.get('account_type_id', 1)  # Default to Free account type

    new_user = User(username=username, email=email, password=password, account_type_id=account_type_id)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Signup successful", "user_id": new_user.user_id})

@app.route('/chatbot')
def chatbot():
    greeting = random.choice(GREETING_RESPONSES)
    return render_template('chatbot.html', greeting=greeting)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message').strip().lower()
    user_id = request.json.get('user_id')  # Fetch user_id if available

    # Define strong negative emotion keywords
    negative_emotion_keywords = ["depressed", "sad", "anxious", "lonely", "hopeless", "angry", "worried"]

    # Check for resources request
    if "resources" in user_message or "help" in user_message:
        resources_reply = "Here are some resources you might find helpful:<br>"
        for resource in RESOURCES:
            resources_reply += f'<a href="{resource["link"]}" target="_blank">{resource["title"]}</a><br>'
        return jsonify({"reply": resources_reply})

    # Check for strong negative emotion keywords
    if any(keyword in user_message for keyword in negative_emotion_keywords):
        reply = random.choice([
            "I'm really sorry you're feeling this way. I'm here to listen.",
            "It’s okay to feel this way sometimes. Please take your time to share more.",
            "I'm here to support you. How can I help?",
            "I’m really sorry to hear that. Do you want to talk more about it?",
            "You’re not alone in this. Please let me know how I can help.",
            "That sounds tough. I’m here for you if you want to share more.",
            "It’s okay to have these feelings. I’m here to listen and support you.",
            "Take your time. Let me know what’s on your mind.",
            "I hear you, and I want to help. Can you tell me more about what you’re going through?",
            "Please remember, you're not alone. I'm here to help and listen."
        ])
        if user_id:
            save_chat_session(user_id, user_message, reply)
        return jsonify({"reply": reply})

    # Check if the message is a greeting
    if any(keyword in user_message for keyword in GREETING_KEYWORDS):
        reply = random.choice(GREETING_RESPONSES)
    # Check for conversation triggers
    elif any(keyword in user_message for keyword in CONVERSATION_KEYWORDS):
        reply = random.choice(CONVERSATION_RESPONSES)
    else:
        # Perform sentiment analysis
        sentiment_analysis = TextBlob(user_message)
        sentiment = sentiment_analysis.sentiment.polarity

        if sentiment > 0:
            responses = [
                "That's wonderful! What made you happy?",
                "I love to hear that! Can you tell me more about it?",
                "Amazing! Keep the positive vibes going!",
                "That sounds great! What else happened?",
                "I'm glad to hear that. What was the highlight?",
                "That’s awesome! What made it so special?",
                "Sounds like you had a fantastic time! Tell me more.",
                "Wow, that's lovely. How did it make you feel?",
                "That’s so nice! What’s next for you?",
                "I’m happy to hear that! Anything else exciting?"
            ]
        elif sentiment < 0:
            responses = [
                "I'm sorry to hear that. Would you like to share more?",
                "It's okay to feel this way sometimes. I'm here to help.",
                "I'm here to listen if you'd like to talk more.",
                "That must be tough. How can I support you?",
                "I’m sorry you’re feeling this way. What’s been on your mind?",
                "I understand this might be hard. Want to talk about it?",
                "Take your time; I’m here for you.",
                "Sometimes it helps to talk things out. How can I assist?",
                "What’s been weighing on you lately?",
                "I’m here to support you. Would you like any resources?"
            ]
        else:
            responses = [
                "Interesting! Tell me more about it.",
                "I see. Could you elaborate on that?",
                "I'm here to understand better. Feel free to share more.",
                "That sounds intriguing. What else can you share?",
                "I’m curious about that. Can you explain more?",
                "Tell me more so I can understand better.",
                "That’s unique! What do you think about it?",
                "I’d love to hear more details about that.",
                "Can you expand on that for me?",
                "I’m here to listen. Go ahead and tell me more."
            ]

        reply = random.choice(responses)

    # Save chat session to the database
    if user_id:
        save_chat_session(user_id, user_message, reply)

    return jsonify({"reply": reply})

def save_chat_session(user_id, user_message, reply):
    new_session = ChatSession(user_id=user_id, chat_log=f"User: {user_message}\nBot: {reply}")
    db.session.add(new_session)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if not already created
    app.run(debug=True)
