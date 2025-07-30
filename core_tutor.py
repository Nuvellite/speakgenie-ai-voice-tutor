import os
import pyaudio 
import wave    
from pydub import AudioSegment
from pydub.playback import play 
from dotenv import load_dotenv

from openai import OpenAI 

# --- Global Language Variable (Can be set by Streamlit) ---
current_ai_language = "English" 

# --- API Key Loading ---
load_dotenv()

# --- Audio Configuration (parameters for recording/saving, not direct I/O) ---
FORMAT = pyaudio.paInt16 
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5 
OUTPUT_FILENAME = "recorded_audio.wav"
AI_RESPONSE_AUDIO_FILENAME = "ai_response.mp3" 

# --- Function to Record Audio from Microphone ---
def record_audio(filename, record_seconds=RECORD_SECONDS):
    """Records audio from the default microphone and saves it to a WAV file.
    This function is primarily for console-based app, Streamlit uses st.audio_recorder."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print(f"\nRecording for {record_seconds} seconds... Speak now!")
    frames = []
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Audio saved to {filename}")
    return filename

# --- Function to Play Audio File ---
def play_audio(filename):
    """Plays an audio file using pydub.
    This function is primarily for console-based app, Streamlit uses st.audio()."""
    try:
        song = AudioSegment.from_file(filename) 
        print(f"Playing {filename}...")
        play(song)
        print("Finished playing.")
    except FileNotFoundError:
        print(f"Error: Audio file '{filename}' not found. Make sure it exists.")
    except Exception as e:
        print(f"An error occurred during playback: {e}")

# --- Function to Transcribe Audio using OpenAI Whisper ---
def transcribe_audio(client_obj, audio_file_path):
    """Transcribes audio from a file using OpenAI Whisper."""
    print(f"Transcribing audio using OpenAI Whisper: {audio_file_path}...")
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = client_obj.audio.transcriptions.create( 
                model="whisper-1",
                file=audio_file,
                language="en" # Force transcription to English
            )
        text = transcription.text
        print(f"Transcription: {text}")
        return text
    except Exception as e:
        print(f"Error during Whisper transcription: {e}")
        return None

# --- Function to Get AI Response from OpenAI GPT ---
def get_gpt_response(client_obj, prompt_text, conversation_history, mode="chat", roleplay_context=""):
    """Gets an AI response from GPT, with optional translation and general child-appropriate persona."""
    print(f"Getting AI response from GPT for: '{prompt_text}' (Mode: {mode})...")
    global current_ai_language 

    try:
        system_message_content = ""
        
        # General child persona (age-specific parts removed)
        general_child_instruction = " You are talking to a young child (aged 5-10)."
        simple_vocab_instruction = "Use words and concepts a 5-10 year old child would easily understand."

        if mode == "chat":
            system_message_content = (
                f"You are SpeakGenie, a friendly, encouraging, and patient English tutor."
                f"{general_child_instruction} Your responses should be simple, positive, and easy for them to understand. "
                f"{simple_vocab_instruction} "
                "Use short sentences and avoid complex vocabulary. "
                "Encourage them to speak and ask simple follow-up questions. "
                "Make learning fun! For factual questions, explain them in a very simple, fun way. "
                "Always include relevant and positive emojis in your responses to make them more engaging! ✨😊📚"
            )
        elif mode == "roleplay":
            system_message_content = (
                f"You are SpeakGenie, a kind and helpful AI English tutor in Roleplay Mode."
                f"{general_child_instruction} Your current scenario is: '{roleplay_context}'. "
                "You must strictly act as the character appropriate to this scenario. "
                f"{simple_vocab_instruction} "
                "Stay in character always! Encourage the child to speak with simple questions. "
                "Keep the conversation friendly, positive, and directly related to the roleplay. "
                "If the child tries to exit or change the topic, gently guide them back to the scenario or remind them to say 'exit roleplay'."
            )
        
        system_message = {"role": "system", "content": system_message_content}
        
        messages = [system_message] + conversation_history + [{"role": "user", "content": prompt_text}]

        if current_ai_language != "English":
            messages.append({"role": "system", "content": f"After your English response, provide a translation into {current_ai_language}. Format: 'English Response. ({current_ai_language} Translation)'"})
        
        chat_completion = client_obj.chat.completions.create( 
            model="gpt-3.5-turbo", # Final model for stability
            messages=messages
        )
        ai_response = chat_completion.choices[0].message.content
        print(f"AI Response: {ai_response}")
        return ai_response
    except Exception as e:
        print(f"Error getting GPT response: {e}")
        return None

# --- Function to Convert Text to Speech using OpenAI TTS ---
def text_to_speech_openai(client_obj, text, filename=AI_RESPONSE_AUDIO_FILENAME, voice="alloy"):
    """Converts text to speech using OpenAI TTS and saves/plays the audio (for console testing)."""
    print(f"Converting AI response to speech using OpenAI TTS (voice: {voice})...")
    try:
        response = client_obj.audio.speech.create(
            model="tts-1", 
            voice=voice,   
            input=text,
        )
        
        response.stream_to_file(filename)
        print(f"AI response audio saved to {filename}")
        
        play_audio(filename) 
        print("AI response played.")
        return filename
    except Exception as e:
        print(f"Error during OpenAI TTS: {e}")
        return None

# --- Functions for managing language selection ---
def set_global_language(language_name): 
    """Sets the global AI response language. Called by Streamlit UI."""
    global current_ai_language
    current_ai_language = language_name
    print(f"AI response language set to {current_ai_language}.")
    return f"Language set to {language_name}."

# --- Helper function to manage a conversation turn for Streamlit ---
def handle_conversation_turn(client_obj, user_input_text, current_conversation_history, current_mode, current_roleplay_context=""):
    """Handles one turn of conversation: gets AI response, updates history, generates speech bytes for Streamlit."""
    
    ai_response_text = None
    ai_audio_bytes = None
    
    print(f"DEBUG: handle_conversation_turn called. Mode: {current_mode}, Context: {current_roleplay_context}, Input: '{user_input_text}'") # DEBUG
    
    # --- Rule-based interceptor for critical roleplay persona breaks ---
    # This part tries to provide a hardcoded in-character response if certain phrases are detected.
    # It only triggers for the Store roleplay and for very early turns.
    if current_mode == "roleplay_mode" and \
       current_roleplay_context == "At the Store: You are buying something from a helpful shopkeeper. Focus on asking for items and quantities." and \
       len(current_conversation_history) < 3: # Only intercept for first few turns
        
        lower_input = user_input_text.lower()
        print(f"DEBUG: Store interceptor active. Lower input: '{lower_input}'") # DEBUG

        if "can i get" in lower_input or "do you have" in lower_input or "where is" in lower_input or "i need" in lower_input:
            print("DEBUG: Interceptor caught a request phrase.") # DEBUG
            if "pen" in lower_input:
                ai_response_text = "Certainly! We have many pens. What color pen would you like? 🖊️"
            elif "book" in lower_input:
                ai_response_text = "Of course! What kind of book are you looking for? A storybook or a drawing book? 📚"
            elif "apple" in lower_input:
                ai_response_text = "Apples are delicious! How many apples would you like? 🍎"
            elif "pet" in lower_input: 
                ai_response_text = "Oh, a pet! We don't sell pets here in this store, but we have lovely books about animals! 🐾"
            else: # General fallback for any other item asked about in the store
                ai_response_text = "Hmm, let me check for you! What exactly are you looking for? ✨"
            
            # If a hardcoded response was generated by any of the above conditions
            if ai_response_text: 
                print(f"DEBUG: Hardcoded response chosen: '{ai_response_text}'") # DEBUG
                current_conversation_history.append({"role": "user", "content": user_input_text})
                current_conversation_history.append({"role": "assistant", "content": ai_response_text})
                
                try:
                    audio_stream = client_obj.audio.speech.create(
                        model="tts-1", 
                        voice="alloy",   
                        input=ai_response_text,
                        response_format="mp3" 
                    )
                    ai_audio_bytes = audio_stream.read() 
                    print("DEBUG: Hardcoded audio generated. Returning.") # DEBUG
                    return ai_response_text, current_conversation_history, ai_audio_bytes
                except Exception as e:
                    print(f"Error generating speech bytes for Streamlit (hardcoded response): {e}")
                    current_conversation_history.append({"role": "user", "content": user_input_text})
                    current_conversation_history.append({"role": "assistant", "content": ai_response_text})
                    print("DEBUG: Hardcoded audio failed. Returning.") # DEBUG
                    return ai_response_text, current_conversation_history, None 
    # --- END Rule-based Interceptor Logic ---

    # If no hardcoded response was returned, proceed to call GPT as usual
    print(f"DEBUG: Interceptor did NOT trigger a return. Calling GPT.") # DEBUG
    ai_response_text = get_gpt_response(client_obj, user_input_text, current_conversation_history, mode=current_mode, roleplay_context=current_roleplay_context)
    
    if ai_response_text:
        current_conversation_history.append({"role": "user", "content": user_input_text})
        current_conversation_history.append({"role": "assistant", "content": ai_response_text})
        
        try:
            audio_stream = client_obj.audio.speech.create(
                model="tts-1", 
                voice="alloy",   
                input=ai_response_text,
                response_format="mp3" 
            )
            audio_bytes = audio_stream.read() 
            return ai_response_text, current_conversation_history, audio_bytes
        except Exception as e:
            print(f"Error generating speech bytes for Streamlit: {e}")
            return ai_response_text, current_conversation_history, None 
    else:
        return None, current_conversation_history, None
