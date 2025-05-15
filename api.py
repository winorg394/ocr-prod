import os
import json
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from ocr import process_file  # Fixed import statement - removed process_base64
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure required environment variables are set
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("OPENAI_API_KEY environment variable is not set")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'.jpg', '.jpeg', '.png', '.pdf'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed"""
    file_extension = os.path.splitext(filename)[1].lower()
    return file_extension in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/extract', methods=['POST'])
def extract_info():
    """API endpoint to extract information from uploaded file"""
    # Print request details for debugging
    print(f"Request Content-Type: {request.content_type}")
    print(f"Request form data: {request.form}")
    print(f"Request files: {request.files}")
    
    # Check if file part exists in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file extension is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported'}), 400
    
    # Get model from request or use default
    model = request.form.get('model', 'deepseek/DeepSeek-V3-0324')
    
    # Save file to uploads folder
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Process the file
    try:
        result = process_file(file_path, model)
        # Try to parse the result as JSON
        try:
            result_json = json.loads(result)
            return jsonify(result_json)
        except json.JSONDecodeError:
            # If result is not valid JSON, clean it up with regex to remove markdown code block markers
            import re
            cleaned_result = re.sub(r'^```json\s*|\s*```$', '', result.strip())
            print(f"Cleaned result: {cleaned_result}")
            
            # Try to parse the cleaned result as JSON
            try:
                cleaned_json = json.loads(cleaned_result)
                return jsonify(cleaned_json)
            except json.JSONDecodeError:
                # If still not valid JSON, return as text
                return cleaned_result, 200, {'Content-Type': 'application/json'}
            
            return jsonify({result})
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Error processing file: {str(e)}")
        print(error_traceback)
        return jsonify({'error': str(e), 'traceback': error_traceback}), 500
    finally:
        # Optionally, remove the file after processing
        # Uncomment the following lines if you want to delete files after processing
        pass  # Added this line to fix the indentation error after finallysdfsdf

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True,host='0.0.0.0', port=port)