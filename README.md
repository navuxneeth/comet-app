# Comet App

A Flask-based AI assistant application that combines OpenAI and Google Gemini APIs to provide conversational AI with voice support and image/document analysis capabilities.

## Features

- **Conversational AI**: Chat with an AI assistant using text or voice input
- **Voice Interaction**: Record audio messages and receive spoken responses using OpenAI's Whisper and TTS
- **Vision Analysis**: Upload images or PDFs for AI-powered analysis using Google Gemini
- **Camera Capture**: Take photos directly within the app for analysis
- **Multiple Tone Options**: Choose from friendly, professional, creative, or concise conversation styles
- **Dark/Light Theme**: Toggle between dark and light modes
- **Conversation History**: Maintain context throughout your chat session

## Prerequisites

- Python 3.7+
- OpenAI API key
- Google Gemini API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/navuxneeth/comet-app.git
   cd comet-app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5001`

3. Click the settings icon (⚙️) and enter your API keys:
   - OpenAI API key (for chat and voice features)
   - Google Gemini API key (for vision/image analysis)

4. Start chatting! You can:
   - Type messages in the text input
   - Click the microphone button (🎤) to record voice messages
   - Click the attachment button (📎) to upload images/PDFs or take photos

## Configuration

### Tone Selection

Click the tone icon in the header to choose your preferred conversation style:
- 😊 **Friendly**: Casual, warm, and approachable
- 👔 **Professional**: Formal, structured, and precise
- 🎨 **Creative**: Imaginative, witty, and expressive
- ⚡️ **Concise**: Direct, brief, and to-the-point

### Theme

Click the sun/moon icon (☀️/🌙) to toggle between light and dark modes.

## Dependencies

- Flask - Web framework
- OpenAI - Chat, transcription, and text-to-speech
- google-generativeai - Vision and image analysis
- pypdfium2 - PDF processing
- Pillow - Image handling

## License

MIT License
