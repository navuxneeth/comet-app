# Simple Gemini Chat App
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
import json
import os

# Initialize Flask
app = Flask(__name__)

# Configure Gemini API - Use environment variable or hardcoded key
# Get your free API key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyD6RTduliVvqtOmJP04dEH2h2LqhvnHxGE")
genai.configure(api_key=GEMINI_API_KEY)

# Set request timeout (in seconds)
REQUEST_TIMEOUT = 30

# Initialize the model - use gemini-1.5-flash (gemini-pro is deprecated)
model = genai.GenerativeModel('gemini-1.5-flash')
vision_model = genai.GenerativeModel('gemini-1.5-flash')  # For vision tasks

# Tone system prompts
def get_system_prompt(tone='friendly'):
    prompts = {
        'professional': "You are a highly professional and formal assistant. Your responses are structured, precise, and use formal language. You are named Comet.",
        'creative': "You are a witty and creative assistant. You often use metaphors and imaginative language to explain things. You are named Comet.",
        'concise': "You are a direct and concise assistant. You get straight to the point and avoid any filler or unnecessary words. You are named Comet.",
        'friendly': "You are a helpful, friendly, and concise assistant named Comet."
    }
    return prompts.get(tone, prompts['friendly'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint to verify server is running."""
    return jsonify({"status": "ok", "api_key_configured": bool(GEMINI_API_KEY)})

@app.route('/process-chat', methods=['POST'])
def process_chat():
    try:
        user_prompt = request.form.get('text', '')
        tone = request.form.get('tone', 'friendly')
        conversation_history = json.loads(request.form.get('conversationHistory', '[]'))
        
        if not user_prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        # Build conversation context
        context = get_system_prompt(tone) + "\n\n"
        for msg in conversation_history:
            role = "User" if msg['role'] == 'user' else "Assistant"
            context += f"{role}: {msg['content']}\n"
        context += f"User: {user_prompt}\nAssistant:"
        
        # Get response from Gemini with safety settings and timeout
        response = model.generate_content(
            context,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2048,
            ),
            request_options={"timeout": REQUEST_TIMEOUT}
        )
        
        # Handle response - check if there's text
        if response.text:
            ai_response = response.text
        elif response.candidates and response.candidates[0].content.parts:
            ai_response = response.candidates[0].content.parts[0].text
        else:
            ai_response = "I'm sorry, I couldn't generate a response. Please try again."
        
        return jsonify({
            "user_prompt": user_prompt,
            "assistant_response": ai_response
        })
    
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper() or "INVALID" in error_msg.upper():
            return jsonify({"error": "API key issue. Please check your Gemini API key."}), 500
        if "timeout" in error_msg.lower() or "deadline" in error_msg.lower():
            return jsonify({"error": "Request timed out. Please try again."}), 500
        return jsonify({"error": f"Error: {error_msg}"}), 500

@app.route('/process-vision', methods=['POST'])
def process_vision():
    try:
        tone = request.form.get('tone', 'friendly')
        
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        file_bytes = file.read()
        
        # Check if it's an image
        if not file.mimetype.startswith('image/'):
            return jsonify({"error": "Only image files are supported"}), 400
        
        # Prepare the image for Gemini
        import PIL.Image
        import io
        image = PIL.Image.open(io.BytesIO(file_bytes))
        
        # Create prompt with tone
        prompt = f"{get_system_prompt(tone)}\n\nWhat do you see in this image? Describe it in detail."
        
        # Get response from Gemini vision model with timeout
        response = vision_model.generate_content(
            [prompt, image],
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2048,
            ),
            request_options={"timeout": REQUEST_TIMEOUT}
        )
        
        # Handle response
        if response.text:
            ai_response = response.text
        elif response.candidates and response.candidates[0].content.parts:
            ai_response = response.candidates[0].content.parts[0].text
        else:
            ai_response = "I couldn't analyze this image. Please try another image."
        
        return jsonify({
            "assistant_response": ai_response
        })
    
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper() or "INVALID" in error_msg.upper():
            return jsonify({"error": "API key issue. Please check your Gemini API key."}), 500
        if "timeout" in error_msg.lower() or "deadline" in error_msg.lower():
            return jsonify({"error": "Request timed out. Please try again."}), 500
        return jsonify({"error": f"Vision error: {error_msg}"}), 500

if __name__ == '__main__':
    print("🚀 Starting Comet Assistant with Gemini API...")
    print("📍 Open http://localhost:5001 in your browser")
    app.run(debug=True, port=5001)