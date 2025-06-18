import streamlit as st
import os
import tempfile
from audio_recorder_streamlit import audio_recorder
from groq_client import GroqClient
from voice_handler import VoiceHandler
import numpy as np
import soundfile as sf

# Page configuration
st.set_page_config(
    page_title="AI Voice Bot",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
        color: #333;   /* Explicit text color */
    }
    .claude-message {
        background-color: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #9c27b0;
        color: #333;   /* Explicit text color */
    }
    .sample-questions {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ff9800;
        color: #333;   /* Explicit text color */
    }
    /* Add this to fix all text colors */
    body {
        color: #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'recorder_key' not in st.session_state:
    st.session_state.recorder_key = 0
if 'groq_client' not in st.session_state:
    try:
        st.session_state.groq_client = GroqClient()
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {e}")
        st.stop()
if 'voice_handler' not in st.session_state:
    st.session_state.voice_handler = VoiceHandler()

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎤 AI Voice Bot</h1>
        <p>Have a conversation with an AI assistant using voice or text!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with instructions and sample questions
    with st.sidebar:
        st.header("📋 Instructions")
        st.write("""
        1. **Voice Input**: Click the microphone button and speak your question
        2. **Text Input**: Type your question in the text box
        3. **Listen**: Click the play button to hear the AI's response
        4. **Clear**: Use the button to start a new conversation
        """)
        
        st.header("🎯 Sample Questions")
        st.markdown("""
        <div class="sample-questions">
        <ul>
            <li>What should we know about your life story in a few sentences?</li>
            <li>What's your #1 superpower?</li>
            <li>What are the top 3 areas you'd like to grow in?</li>
            <li>What misconception do people have about you?</li>
            <li>How do you push your boundaries and limits?</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice settings
        st.header("🔊 Voice Settings")
        voices = st.session_state.voice_handler.get_available_voices()
        if voices:
            voice_options = {name: voice_id for voice_id, name in voices}
            selected_voice = st.selectbox("Select Voice", list(voice_options.keys()))
            if st.button("Apply Voice"):
                if st.session_state.voice_handler.set_voice(voice_options[selected_voice]):
                    st.success("Voice updated!")
                else:
                    st.error("Failed to update voice")
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("💬 Conversation")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="claude-message">
                        <strong>AI Assistant:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add audio player for AI responses
                    if "audio_path" in message:
                        st.audio(message["audio_path"])
    
    with col2:
        st.header("🎤 Input")
        
        # Voice input
        st.subheader("Voice Input")
        
        # Add key parameter to audio_recorder
        audio_bytes = audio_recorder(
            pause_threshold=2.0,  # Wait longer before stopping
            text="Click and speak clearly",
            recording_color="#e74c3c",
            neutral_color="#34495e",
            icon_name="microphone",
            icon_size="2x",
            key=f"recorder_{st.session_state.recorder_key}"  # Add this key parameter
        )
        
        if audio_bytes:
            # Show audio player immediately
            st.audio(audio_bytes, format="audio/wav")
            
            # Get the recognized text using test_recognition
            user_input = st.session_state.voice_handler.test_recognition(audio_bytes)
            
            # Display the recognition result
            st.write(f"Recognized text: {user_input}")
            
            # Check if recognition was successful
            if user_input and not user_input.startswith("Recognition failed"):
                # Increment recorder key to reset the widget
                st.session_state.recorder_key += 1
                
                # Process the input
                process_user_input(user_input)
            else:
                st.warning("Could not recognize speech. Please try again.")
        
        # Text input
        st.subheader("Text Input")
        user_text = st.text_area("Type your question here:", height=100)
        
        if st.button("Send", type="primary"):
            if user_text.strip():
                process_user_input(user_text)
            else:
                st.warning("Please enter a question!")

def process_user_input(user_input):
    """Process user input and generate Claude's response"""
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    with st.spinner("Thinking..."):
        try:
            ai_response = st.session_state.groq_client.get_response(user_input)
            
            # Generate audio for the response
            audio_path = st.session_state.voice_handler.text_to_speech(ai_response)
            
            # Verify audio file
            if audio_path and os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                # Add response to chat
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response,
                    "audio_path": audio_path
                })
            else:
                # Add response without audio
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response
                })
                st.warning("Audio response could not be generated")
            
            # DON'T rerun here - let Streamlit handle it naturally
            # Removed st.rerun() to prevent widget state issues
            
        except Exception as e:
            st.error(f"Error getting response: {e}")

if __name__ == "__main__":
    main()