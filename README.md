# Comet Assistant 🌐

A simple AI chat assistant powered by **Google Gemini**. Ready to use immediately with a working API key!

## ✨ Features

- **💬 Text Chat**: Conversation with Google Gemini AI
- **🎨 Multiple Tones**: Choose from Friendly, Professional, Creative, or Concise styles
- **📸 Vision Analysis**: Upload and analyze images using Gemini vision
- **🌙 Dark/Light Theme**: Toggle between dark and light modes
- **📝 Conversation History**: Maintains context throughout your chat session
- **📷 Camera Capture**: Take photos for analysis

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
Or double-click `setup.bat` on Windows

### 2. Run the App
```bash
python app.py
```
Or double-click `start.bat` on Windows

### 3. Open in Browser
Navigate to: **http://localhost:5001**

**That's it!** Start chatting immediately 🎉

## 🔑 API Key

The app comes with a pre-configured Gemini API key. If you need to use your own:

1. Get a free API key from: https://aistudio.google.com/app/apikey
2. Set it as an environment variable:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   python app.py
   ```
   Or edit `app.py` directly and replace the API key.

## 📋 What Works

✅ **Text Chat** - Powered by Google Gemini (gemini-1.5-flash)  
✅ **Image Analysis** - Gemini vision capabilities  
✅ **4 Tone Modes** - Friendly, Professional, Creative, Concise  
✅ **Theme Switching** - Light and dark modes  
✅ **Conversation History** - Maintains context  
✅ **Camera Capture** - Take photos for analysis  

## ⚙️ Tech Stack

- **Backend**: Python Flask
- **AI**: Google Gemini API (gemini-1.5-flash)
- **Frontend**: Vanilla JavaScript + HTML/CSS
- **Styling**: Custom CSS with dark mode support

## 📦 Dependencies

```
Flask
google-generativeai
Pillow
```

## 💡 How It Works

The app uses Google Gemini API with a hardcoded API key, so you don't need to set up anything. Just install and run!

## 🎯 Features

- **No Setup**: Works immediately
- **Free to Use**: No API costs for users (Gemini has generous free tier)
- **Vision Support**: Analyze images with Gemini
- **Context Aware**: Remembers conversation history
- **Multiple Tones**: Adapt AI personality

## 💡 Usage Tips

1. **Start a new chat**: Click the ＋ icon in the header
2. **Change tone**: Click the emoji icon to select conversation style
3. **Upload images**: Click the + button next to the input field
4. **Toggle theme**: Click the ☀️/🌙 icon
5. **Clear history**: Open settings (⚙️) and click "Clear History"

## 🔧 Troubleshooting

If you get errors like "INTERNAL SERVER ERROR":
1. Check your internet connection
2. Verify the API key is valid (get one from https://aistudio.google.com/app/apikey)
3. Make sure the `gemini-1.5-flash` model is available in your region

## 📄 License

MIT License

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

Made with ❤️ using Google Gemini API
