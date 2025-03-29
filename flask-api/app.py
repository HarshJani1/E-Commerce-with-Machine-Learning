from flask import Flask, request, jsonify
import pickle
import re
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import os

app = Flask(__name__)

nltk.download('stopwords')

with open('models/svm_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

with open('models/tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    loaded_vectorizer = pickle.load(vectorizer_file)

ps = PorterStemmer()
all_stopwords = stopwords.words('english')
all_stopwords.remove('not') 

def preprocess_text(text):
    """Clean and preprocess text for sentiment analysis"""
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [ps.stem(word) for word in text if word not in all_stopwords]
    return ' '.join(text)

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """Endpoint for sentiment analysis"""
    try:
        data = request.get_json()
        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        processed_text = preprocess_text(data['text'])
        transformed_text = loaded_vectorizer.transform([processed_text]).toarray()
        prediction = int(loaded_model.predict(transformed_text)[0])  
        
        return jsonify({
            'sentiment': prediction,
            'processed_text': processed_text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)