from flask import Flask, request, jsonify
import fetchData
import pdfplumber
from io import BytesIO


app = Flask(__name__)

@app.route('/analyze-pdf', methods=['POST'])
def analyze_pdf_endpoint():
    try:
        # Retrieve the file from the request
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file provided"}), 400

        # Read the PDF content using pdfplumber
        with pdfplumber.open(BytesIO(file.read())) as pdf:
            raw_text = ""
            for page in pdf.pages:
                raw_text += page.extract_text() or ""

        # Call the analyze_pdf function
        result = fetchData.analyze_pdf(raw_text)

        # Return the result as JSON
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask-question', methods=['POST'])
def analyze_question_endpoint():
    try:
        data = request.json
        if 'question' not in data:
            return jsonify({"error": "No question provided"}), 400
        
        # Extract the question from the data
        question = data['question']
        
        # Placeholder for analysis logic (replace with your analysis code)
        response = fetchData.analyze_question(question)
        
        # Return the response as JSON
        return jsonify({"response": response}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
