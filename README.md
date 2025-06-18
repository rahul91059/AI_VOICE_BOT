# AI Voice Bot (Powered by Groq - FREE!)

![image](https://github.com/user-attachments/assets/4f6ca1af-cccb-469a-9f3b-22635ee65a44)



A voice-enabled chatbot that responds naturally and helpfully, built with Streamlit and Groq's FREE API.

## Features

- 🎤 **Voice Input**: Speak your questions using the microphone
- 💬 **Text Input**: Type your questions if you prefer
- 🔊 **Voice Output**: Hear the AI's responses with text-to-speech
- 🎯 **Natural Conversations**: Designed to respond authentically and helpfully
- 🎨 **User-Friendly Interface**: Simple, intuitive web interface
- 💰 **Completely FREE**: Uses Groq's free API with generous limits


## Setup Instructions

### 1. Get Your FREE Groq API Key

1. Go to [console.groq.com](https://console.groq.com/)
2. Sign up for a FREE account (no credit card required!)
3. Go to API Keys section
4. Create your API key
5. Copy the key (starts with `gsk_`)

### 2. Install Dependencies

Open a terminal in your project directory and run:

```bash
pip install -r requirements.txt
```

**Note**: If you encounter issues with `pyaudio`, try:
- On Windows: `pip install pipwin && pipwin install pyaudio`
- On macOS: `brew install portaudio && pip install pyaudio`
- On Linux: `sudo apt-get install python3-pyaudio`

### 3. Configure API Key

1. Open the `.env` file
2. Replace `your_groq_api_key_here` with your actual API key:
   ```
   GROQ_API_KEY=gsk_your-actual-key-here
   ```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## How to Use

### Voice Input
1. Click the microphone button
2. Speak your question clearly
3. Wait for processing
4. The AI will respond with both text and voice

### Text Input
1. Type your question in the text area
2. Click "Send"
3. The AI will respond with text and voice

### Sample Questions to Try
- "What should we know about your life story in a few sentences?"
- "What's your #1 superpower?"
- "What are the top 3 areas you'd like to grow in?"
- "What misconception do people have about you?"
- "How do you push your boundaries and limits?"

## Troubleshooting

### Common Issues

**1. API Key Error**
- Make sure your API key is correctly set in the `.env` file
- Groq offers generous free limits, so you shouldn't hit rate limits easily

**2. Microphone Not Working**
- Check browser permissions for microphone access
- Try refreshing the page

**3. Audio Dependencies**
- If audio recording/playback doesn't work, try reinstalling audio dependencies:
  ```bash
  pip uninstall pyaudio pyttsx3
  pip install pyaudio pyttsx3
  ```

**4. Import Errors**
- Make sure all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

### System Requirements
- Python 3.7+
- Microphone access
- Internet connection
- Modern web browser (Chrome, Firefox, Safari, Edge)

## File Structure

```
VoiceBot/
├── app.py                 # Main Streamlit application
├── groq_client.py         # Groq API integration (FREE!)
├── voice_handler.py       # Voice processing (STT/TTS)
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (API keys)
└── README.md            # This file
```

## Privacy & Security

- Your API key is stored locally in the `.env` file
- Conversations are not stored permanently
- Audio processing happens locally on your machine
- No data is shared with third parties except for the Claude API calls

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify your API key is correctly configured
4. Check your internet connection

For Groq API specific issues, consult the [Groq documentation](https://console.groq.com/docs/quickstart).
