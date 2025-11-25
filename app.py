# Simple Gemini Chat App
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
import json

# Initialize Flask
app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCnIzEvA2p1NBicc2rb_drzIr2k1M-6HkQ"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model - try gemini-pro first, will auto-detect available models
try:
    model = genai.GenerativeModel('gemini-pro')
except:
    # If gemini-pro doesn't work, try gemini-1.5-flash
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
        
        # Get response from Gemini
        response = model.generate_content(context)
        ai_response = response.text
        
        return jsonify({
            "user_prompt": user_prompt,
            "assistant_response": ai_response
        })
    
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

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
        
        # Get response from Gemini vision model
        response = vision_model.generate_content([prompt, image])
        
        return jsonify({
            "assistant_response": response.text
        })
    
    except Exception as e:
        return jsonify({"error": f"Vision error: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting Comet Assistant with Gemini API...")
    print("📍 Open http://localhost:5001 in your browser")
    app.run(debug=True, port=5001)