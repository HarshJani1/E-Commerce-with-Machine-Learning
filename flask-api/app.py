from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import logging
from waitress import serve

# Initialize Flask app
app = Flask(__name__)

# Configure CORS - allow all origins for development
CORS(app, resources={r"/*": {"origins": "*"}})


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Initialize stemmer and stopwords
ps = PorterStemmer()
all_stopwords = set(stopwords.words('english')) - {'not'}

# Load ML models
try:
    with open('models/svm_model.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    with open('models/tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
        loaded_vectorizer = pickle.load(vectorizer_file)
    logger.info("ML models loaded successfully")
except Exception as e:
    logger.error(f"Error loading model files: {str(e)}")
    raise RuntimeError("Failed to load model files") from e


def preprocess_text(text):
    """Enhanced text preprocessing with error handling"""
    try:
        # Preserve contractions and handle special characters better
        text = re.sub(r"[^a-zA-Z']", ' ', text)
        text = re.sub(r"\s+", ' ', text).strip().lower()

        tokens = text.split()
        processed_tokens = [
            ps.stem(word)
            for word in tokens
            if word not in all_stopwords and len(word) > 2
        ]
        return ' '.join(processed_tokens)
    except Exception as e:
        logger.error(f"Text preprocessing failed: {str(e)}")
        return ""


def _build_cors_preflight_response():
    """Build CORS preflight response"""
    response = jsonify({'message': 'CORS preflight'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response


@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_sentiment():
    """Improved sentiment analysis endpoint"""
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    try:
        # Validate request format
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.get_json()
        if 'text' not in data or not isinstance(data['text'], str):
            return jsonify({'error': 'Invalid or missing text field'}), 400

        text = data['text'].strip()
        if len(text) < 3:
            return jsonify({'error': 'Text must be at least 3 characters'}), 400

        # Process and validate text
        processed_text = preprocess_text(text)
        if not processed_text:
            return jsonify({'error': 'Failed to process text'}), 400

        # Transform and predict
        transformed_text = loaded_vectorizer.transform([processed_text]).toarray()  # Convert to dense array
        prediction = loaded_model.predict(transformed_text)

        # Ensure valid prediction format
        if prediction.size == 0:
            raise ValueError("Empty prediction result")

        sentiment = int(prediction[0])

        return jsonify({
            'sentiment': sentiment,
            'processed_text': processed_text,
            'original_text': text
        })

    except Exception as e:
        logger.error(f"Sentiment analysis error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    logger.info("Starting Flask server...")
    serve(app, host='0.0.0.0', port=5001)