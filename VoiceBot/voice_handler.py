import speech_recognition as sr
import pyttsx3
import streamlit as st
import tempfile
import os
from config import Config
import wave
import io

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 3000  # Increase sensitivity
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8   # Shorter pause detection
        self.tts_engine = pyttsx3.init()
        self._configure_tts()
    
    def _configure_tts(self):
        """Configure text-to-speech settings"""
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Prefer natural-sounding voices
            preferred_voices = ['zira', 'david', 'hazel']
            for voice in voices:
                if any(pv in voice.name.lower() for pv in preferred_voices):
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            else:
                self.tts_engine.setProperty('voice', voices[0].id)
        
        self.tts_engine.setProperty('rate', Config.VOICE_RATE)
        self.tts_engine.setProperty('volume', Config.VOICE_VOLUME)
    
    def speech_to_text(self, audio_bytes):
        """Convert audio bytes to text with proper WAV format handling"""
        try:
            # Create in-memory WAV file
            with io.BytesIO() as wav_buffer:
                with wave.open(wav_buffer, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(16000)  # 16kHz sample rate
                    wav_file.writeframes(audio_bytes)
                
                wav_data = wav_buffer.getvalue()
            
            # Convert to AudioData format
            audio_data = sr.AudioData(
                wav_data, 
                sample_rate=16000, 
                sample_width=2
            )
            
            # Use Google's speech recognition
            text = self.recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand what you said. Could you please try again?"
        except sr.RequestError as e:
            return f"Sorry, there was an error with the speech recognition service: {e}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def test_recognition(self, audio_bytes):
        """Alternative recognition method using temporary file"""
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            
            r = sr.Recognizer()
            with sr.AudioFile(tmp_path) as source:
                audio = r.record(source)
                result = r.recognize_google(audio)
            
            # Clean up temporary file
            try:
                os.unlink(tmp_path)
            except:
                pass
            
            return result  # Return the recognized text directly
        except Exception as e:
            # Clean up temporary file in case of error
            try:
                os.unlink(tmp_path)
            except:
                pass
            return f"Recognition failed: {str(e)}"
    
    def text_to_speech(self, text):
        """Convert text to speech with proper error handling"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_path = tmp_file.name
            
            # Generate and save audio
            self.tts_engine.save_to_file(text, tmp_path)
            self.tts_engine.runAndWait()
            
            # Verify audio was generated
            if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 1024:  # At least 1KB
                return tmp_path
            else:
                st.error("Failed to generate audio response")
                return None
        except Exception as e:
            st.error(f"Error in text-to-speech: {str(e)}")
            return None
    
    def get_available_voices(self):
        """Get list of available TTS voices"""
        voices = self.tts_engine.getProperty('voices')
        return [(voice.id, voice.name) for voice in voices] if voices else []
    
    def set_voice(self, voice_id):
        """Set TTS voice by ID"""
        try:
            self.tts_engine.setProperty('voice', voice_id)
            return True
        except:
            return False