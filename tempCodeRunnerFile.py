from flask import Flask, render_template, request, jsonify, session
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import json
import random
import logging
from datetime import datetime, timedelta
import re
from collections import defaultdict

# Download required NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
print(__name__)
# app.secret_key = 'your-secret-key-here'  # Change this in production

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load configuration data
try:
    with open('states.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except Exception as e:
    logger.error(f"Error loading configuration: {e}")
    raise

class UserManager:
    def __init__(self):
        self.users = {}
        self.mood_history = defaultdict(list)

    def register_user(self, user_data):
        user_id = f"user_{len(self.users) + 1}"
        self.users[user_id] = {
            'details': user_data,
            'created_at': datetime.now(),
            'last_active': datetime.now()
        }
        return user_id

    def update_last_active(self, user_id):
        if user_id in self.users:
            self.users[user_id]['last_active'] = datetime.now()

    def get_user(self, user_id):
        return self.users.get(user_id)

    def add_mood(self, user_id, mood_data):
        self.mood_history[user_id].append({
            'mood': mood_data['mood'],
            'timestamp': datetime.now(),
            'value': mood_data['value']
        })

    def get_mood_history(self, user_id, days=7):
        cutoff = datetime.now() - timedelta(days=days)
        return [mood for mood in self.mood_history[user_id] 
                if mood['timestamp'] > cutoff]

class ResponseGenerator:
    def __init__(self, config):
        self.config = config
        self.sia = SentimentIntensityAnalyzer()
        
    def analyze_sentiment(self, text):
        scores = self.sia.polarity_scores(text)
        return {
            'compound': scores['compound'],
            'sentiment': 'positive' if scores['compound'] > 0.05 
                        else 'negative' if scores['compound'] < -0.05 
                        else 'neutral'
        }
    
    def detect_emergency(self, text):
        emergency_keywords = [
            "suicide", "kill myself", "end my life", "don't want to live",
            "want to die", "hurting myself", "self harm"
        ]
        return any(keyword in text.lower() for keyword in emergency_keywords)

    def generate_response(self, message, user_data=None, mood=None):
        # Check for emergency situations first
        if self.detect_emergency(message):
            return self.generate_emergency_response()

        # Analyze sentiment
        sentiment = self.analyze_sentiment(message)
        
        # Generate appropriate response based on content and sentiment
        if "anxiety" in message.lower() or "anxious" in message.lower():
            return self.generate_themed_response("anxiety")
        elif "depress" in message.lower() or "sad" in message.lower():
            return self.generate_themed_response("depression")
        elif "stress" in message.lower():
            return self.generate_themed_response("stress")
        elif sentiment['sentiment'] == 'positive':
            return self.generate_themed_response("positive")
        else:
            return self.generate_themed_response("neutral")

    def generate_emergency_response(self):
        return {
            'response': (
                "I'm concerned about what you're saying. Remember, you're not alone. "
                "Would you like to talk to someone right now? "
                "The National Crisis Hotline (988) is available 24/7."
            ),
            'resources': self.config['emergency']['hotlines'],
            'type': 'emergency',
            'priority': 'high'
        }

    def generate_themed_response(self, theme):
        responses = self.config['chatbot']['responses'].get(theme, 
                    self.config['chatbot']['responses']['greeting'])
        return {
            'response': random.choice(responses),
            'type': theme
        }

# Initialize managers
user_manager = UserManager()
response_generator = ResponseGenerator(config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register-user', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'age', 'gender', 'state', 'zipCode']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400

        # Validate age
        age = int(data['age'])
        if not (13 <= age <= 100):
            return jsonify({
                'success': False,
                'message': 'Age must be between 13 and 100'
            }), 400

        # Validate ZIP code
        if not re.match(r'^\d{5}$', data['zipCode']):
            return jsonify({
                'success': False,
                'message': 'Invalid ZIP code format'
            }), 400

        # Register user
        user_id = user_manager.register_user(data)
        session['user_id'] = user_id

        return jsonify({
            'success': True,
            'user_id': user_id
        })

    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message')
        user_id = session.get('user_id')

        if not message:
            return jsonify({
                'success': False,
                'message': 'No message provided'
            }), 400

        if not user_id:
            return jsonify({
                'success': False,
                'message': 'User not authenticated'
            }), 401

        # Update user's last active timestamp
        user_manager.update_last_active(user_id)

        # Generate response
        user_data = user_manager.get_user(user_id)
        response_data = response_generator.generate_response(
            message,
            user_data=user_data,
            mood=data.get('currentMood')
        )

        return jsonify({
            'success': True,
            **response_data
        })

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@app.route('/track-mood', methods=['POST'])
def track_mood():
    try:
        data = request.get_json()
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({
                'success': False,
                'message': 'User not authenticated'
            }), 401

        mood_data = {
            'mood': data.get('mood'),
            'value': data.get('value', 3),
            'timestamp': datetime.now()
        }

        user_manager.add_mood(user_id, mood_data)
        mood_history = user_manager.get_mood_history(user_id)

        return jsonify({
            'success': True,
            'mood_history': mood_history
        })

    except Exception as e:
        logger.error(f"Error tracking mood: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@app.route('/get-resources', methods=['POST'])
def get_resources():
    try:
        data = request.get_json()
        mood = data.get('mood', 'neutral')
        
        # Get appropriate resources based on mood
        resources = config.get('resources', {}).get(mood, [])
        
        return jsonify({
            'success': True,
            'resources': resources
        })

    except Exception as e:
        logger.error(f"Error getting resources: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True)