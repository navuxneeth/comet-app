# Save this file as app.py
import openai
import google.generativeai as genai
import json
import base64
import os
import tempfile
from flask import Flask, render_template, request, jsonify
import pypdfium2 as pdfium
from PIL import Image

# --- Initialize Flask App ---
app = Flask(__name__)

# --- Helper Function for Tone-based System Prompts ---
def get_system_prompt(tone='friendly'):
    prompts = {
        'professional': "You are a highly professional and formal assistant. Your responses are structured, precise, and use formal language. You are named Comet.",
        'creative': "You are a witty and creative assistant. You often use metaphors and imaginative language to explain things. You are named Comet.",
        'concise': "You are a direct and concise assistant. You get straight to the point and avoid any filler or unnecessary words. You are named Comet.",
        'friendly': "You are a helpful, friendly, and concise assistant named Comet." # Default
    }
    return prompts.get(tone, prompts['friendly'])

# --- Core AI and Voice Functions ---

def text_to_speech_openai(api_key, text):
    # ... (code is unchanged)
    client = openai.OpenAI(api_key=api_key)
    response = client.audio.speech.create(model="tts-1", voice="nova", input=text)
    return response.content

def get_openai_chat_response(api_key, conversation_history, tone):
    client = openai.OpenAI(api_key=api_key)
    system_message = {"role": "system", "content": get_system_prompt(tone)}
    messages = [system_message] + conversation_history
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    return response.choices[0].message.content

def get_gemini_vision_response(api_key, file_bytes, mime_type, tone):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    content_part = {"mime_type": mime_type, "data": file_bytes}
    # We inject the tone instruction into the prompt for Gemini
    prompt_with_tone = f"Your tone should be {tone}. Describe what you see in this image or document in a helpful way."
    response = model.generate_content([prompt_with_tone, content_part])
    return response.text
    
# --- Flask Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/process-chat', methods=['POST'])
def process_chat_route():
    api_key = request.form.get('apiKey')
    conversation_history = json.loads(request.form.get('conversationHistory', '[]'))
    tone = request.form.get('tone', 'friendly') # Get the tone
    user_prompt = ""

    try:
        # ... (audio/text processing is unchanged)
        if 'audio' in request.files:
            audio_file = request.files['audio']
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                audio_file.save(tmp.name)
                client = openai.OpenAI(api_key=api_key)
                with open(tmp.name, "rb") as f:
                    user_prompt = client.audio.transcriptions.create(model="whisper-1", file=f).text
            os.remove(tmp.name)
        elif 'text' in request.form:
            user_prompt = request.form.get('text')

        if not user_prompt: return jsonify({"error": "No prompt"}), 400

        conversation_history.append({"role": "user", "content": user_prompt})
        # Pass the tone to the AI response function
        ai_response = get_openai_chat_response(api_key, conversation_history, tone)
        audio_data = text_to_speech_openai(api_key, ai_response)
        
        return jsonify({
            "user_prompt": user_prompt,
            "assistant_response": ai_response,
            "assistant_audio_b64": base64.b64encode(audio_data).decode('utf-8')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process-vision', methods=['POST'])
def process_vision_route():
    openai_api_key = request.form.get('openaiApiKey')
    gemini_api_key = request.form.get('geminiApiKey')
    tone = request.form.get('tone', 'friendly') # Get the tone
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    try:
        # ... (file and PDF processing is unchanged)
        file_bytes = file.read()
        mime_type = file.mimetype
        if mime_type == 'application/pdf':
            pdf = pdfium.PdfDocument(file_bytes)
            page = pdf[0]
            pil_image = page.render().to_pil()
            buffer = tempfile.SpooledTemporaryFile()
            pil_image.save(buffer, 'png')
            buffer.seek(0)
            file_bytes = buffer.read()
            mime_type = 'image/png'

        # Pass the tone to the vision response function
        vision_response = get_gemini_vision_response(gemini_api_key, file_bytes, mime_type, tone)
        audio_data = text_to_speech_openai(openai_api_key, vision_response)
        
        return jsonify({
            "assistant_response": vision_response,
            "assistant_audio_b64": base64.b64encode(audio_data).decode('utf-8')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)