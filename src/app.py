from flask import Flask, request, jsonify, render_template
from src.model import load_model, predict_gap

app = Flask(__name__)

# Load the model at startup
model = load_model()


@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for making predictions"""
    if request.method == 'POST':
        if request.is_json:
            # Handle JSON input
            content = request.get_json()
            input_str = content.get('input')
        else:
            # Handle form input
            input_str = request.form.get('input')

        if not input_str:
            return jsonify({'error': 'No input provided'}), 400

        result = predict_gap(model, input_str)
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Invalid input format. Expected format: "region_id, YYYY-MM-DD HH:MM:SS"'}), 400
