import os
import requests
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Set your Gemini API key here
API_KEY =  os.getenv("API_KEY")  # Replace with your actual API key

# The correct URL for the Gemini API
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explain', methods=['POST'])
def explain_code():
    code = request.form['code'].strip()  # Get the code input

    # Log the received code for debugging
    print(f"Received code for explanation: {code}")

    # Prepare the request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Explain the following Python code: {code}"
                    }
                ]
            }
        ]
    }

    # Make a request to the Gemini API
    try:
        response = requests.post(
            GEMINI_API_URL,
            headers={
                'Content-Type': 'application/json',
            },
            json=payload  # Send the payload as JSON
        )

        # Log the response status and content
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract the explanation text
            explanation = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No explanation available.')
            return jsonify({'explanation': explanation})
        else:
            # Handle non-200 responses
            return jsonify({
                'error': f"Error with the API: {response.status_code}",
                'details': response.text
            }), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
