import streamlit as st
import os
import io 
import base64 
import time 
import copy 

# Import audiorecorder
from audiorecorder import audiorecorder

# Import core tutor functions from core_tutor.py
import core_tutor as ct 
from openai import OpenAI 

# --- Page Configuration ---
# Set layout to 'wide' to utilize full screen width for chat
st.set_page_config(page_title="SpeakGenie AI Voice Tutor Demo", layout="wide")

# --- Session State Initialization ---
# This block runs once when the app starts or when session state is cleared
if "openai_api_key_loaded" not in st.session_state:
    ct.load_dotenv() # Load .env variables from project root
    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if st.session_state.openai_api_key:
        try:
            # Initialize OpenAI client and store it in session state for persistence
            st.session_state.openai_client = OpenAI(api_key=st.session_state.openai_api_key)
            st.session_state.openai_api_key_loaded = True
        except Exception as e:
            st.session_state.openai_api_key_loaded = False
            st.error(f"Error initializing OpenAI client with provided key: {e}")
    else:
        st.session_state.openai_api_key_loaded = False
        st.error("Error: OPENAI_API_KEY not found in your .env file. Please ensure it's set in your project directory.")

# Stop the app if API key isn't loaded or client couldn't be initialized
if not st.session_state.openai_api_key_loaded:
    st.info("Please set your OPENAI_API_KEY in the `.env` file in your project directory to run this app.")
    st.stop() # Stop the app if API key isn't loaded/validly initialized

# Initialize other session state variables for conversation and UI
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [] 

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Free Chat" 

if "current_ai_language" not in st.session_state:
    st.session_state.current_ai_language = "English" 
    ct.set_global_language("English") # Set initial global language in core_tutor module

if "selected_roleplay_scenario" not in st.session_state:
    st.session_state.selected_roleplay_scenario = None

# For preventing re-processing of the same audio segment on reruns
if "last_processed_audio_id" not in st.session_state:
    st.session_state.last_processed_audio_id = None

# --- Helper function to display and play audio in Streamlit ---
def display_and_play_audio(audio_bytes, filename="ai_response.mp3"):
    """Displays an audio player and attempts to play audio automatically."""
    st.audio(audio_bytes, format="audio/mp3") 

# --- NEW: Function to get background CSS ---
def get_background_css(image_path):
    """Generates CSS to set a background image with a dark overlay for better text readability."""
    if not os.path.exists(image_path):
        st.warning(f"Background image not found: {image_path}. Using default background.")
        return ""

    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        /* Add a dark, semi-transparent overlay */
        background-color: rgba(0, 0, 0, 0.6); /* Adjust the alpha value (0 to 1) for darkness */
        background-blend-mode: overlay; /* Blends the overlay with the image */
    }}
    /* Ensure all text elements have white color and a text shadow */
    h1, h2, h3, h4, h5, h6, .stMarkdown, .stSelectbox, .stRadio, .stButton, .stTextInput, label {{
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8); /* Slightly darker shadow */
    }}
    .stMarkdown div ul li {{ /* For list items */
        color: white !important;
    }}
    .stMarkdown div p {{ /* For paragraphs */
        color: white !important;
    }}
    .stAudioRecorder button span {{
        color: white !important;
    }}
    /* Keep the chat container semi-transparent */
    .stContainer {{
        background-color: rgba(0, 0, 0, 0.6) !important;
        border-radius: 10px;
        padding: 20px;
    }}
    </style>
    """
    return css

# --- Apply dynamic background based on current mode/scenario ---
current_bg_image = ""
if st.session_state.current_mode == "Free Chat":
    current_bg_image = "backgrounds/free_chat_bg.jpg"
elif st.session_state.current_mode == "Roleplay Mode":
    if st.session_state.selected_roleplay_scenario == '1': # School
        current_bg_image = "backgrounds/classroom_bg.jpg"
    elif st.session_state.selected_roleplay_scenario == '2': # Store
        current_bg_image = "backgrounds/shop_bg.jpg"
    elif st.session_state.selected_roleplay_scenario == '3': # Home
        current_bg_image = "backgrounds/home_bg.jpg"
    else: # Default for roleplay selection screen
        current_bg_image = "backgrounds/roleplay_selection_bg.jpg" 
    
# Apply the CSS if an image path is determined and exists
if current_bg_image and os.path.exists(current_bg_image):
    st.markdown(get_background_css(current_bg_image), unsafe_allow_html=True)
else:
    st.warning("No specific background image set for this mode/scenario or image not found. Using default Streamlit background. Please ensure images are in the 'backgrounds/' folder.")


# --- UI Layout ---
# Centered Title with Logo and Subtitle
col1, col2, col3 = st.columns([1, 4, 1]) # Use columns for centering

with col2: # Place content in the middle column
    # Optional: Add a smaller logo if main one is in sidebar
    # Or remove sidebar logo and place main logo here for central branding

    # If you want to use the logo in the main section instead of sidebar, move 'logo_path' check here
    # For now, let's assume the logo is in the sidebar as per current design.

    st.markdown(
        "<h1 style='text-align: center; color: white; font-size: 3em; text-shadow: 2px 2px 5px rgba(0,0,0,0.7);'>SpeakGenie! 🗣️</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<h2 style='text-align: center; color: white; font-size: 1.5em; text-shadow: 1px 1px 3px rgba(0,0,0,0.6);'>Your Fun AI English Tutor</h2>",
        unsafe_allow_html=True
    )
    st.markdown("---") # Visual separator

# Sidebar for settings
st.sidebar.header("Tutor Settings")

# Mode Selection Radio Buttons
mode_selection = st.sidebar.radio(
    "Choose Mode:",
    ("Free Chat", "Roleplay Mode")
)

# Handle mode change: reset history, selected scenario, and rerun
if mode_selection != st.session_state.current_mode:
    st.session_state.current_mode = mode_selection
    st.session_state.conversation_history = [] # Reset history when mode changes
    st.session_state.selected_roleplay_scenario = None # Reset scenario
    st.rerun() # Force rerun to update UI based on new mode

st.sidebar.markdown("---")

# Language Selection
language_options = ["English", "Hindi", "Tamil", "Marathi", "Gujarati"]
selected_language = st.sidebar.selectbox(
    "Select AI Response Language:",
    options=language_options,
    index=language_options.index(st.session_state.current_ai_language),
    key="language_selector" 
)

# Handle language change: update global variable in core_tutor and provide success message
if selected_language != st.session_state.current_ai_language:
    st.session_state.current_ai_language = selected_language
    ct.set_global_language(selected_language) 
    st.sidebar.success(f"AI language set to {selected_language}!")

st.sidebar.markdown("---")
st.sidebar.info(
    "To record your input, select ""click to record"" button . "
    "Say 'goodbye' or 'exit' or 'exit roleplay' within your audio to end a conversation/scenario."
)

# --- Main Chat Interface ---
st.header(f"Mode: {st.session_state.current_mode}")

# Roleplay Scenario Selection (only if in Roleplay Mode and no scenario selected yet)
if st.session_state.current_mode == "Roleplay Mode" and st.session_state.selected_roleplay_scenario is None:
    st.subheader("Select a roleplay scenario:")
    scenario_options = {
        "1": "At School (Talk to a teacher or friend)",
        "2": "At the Store (Talk to a shopkeeper)",
        "3": "At Home (Talk to a family member)",
        "4": "Back to Main Menu" 
    }
    scenario_choice = st.radio("Choose a scenario:", list(scenario_options.values()), key="scenario_selector")
    
    # Handle scenario start button click
    if st.button("Start Scenario"):
        for key, value in scenario_options.items():
            if value == scenario_choice:
                st.session_state.selected_roleplay_scenario = key
                break
        
        if st.session_state.selected_roleplay_scenario == '4': # Back to Main Menu selected
            st.session_state.current_mode = "Free Chat" 
            st.session_state.conversation_history = [] # Clear history when returning to main menu
            st.session_state.selected_roleplay_scenario = None
            st.rerun() # Rerun to switch mode and clear chat
        else:
            # Define scenario context and initial greetings
            scenario_context_map = {
                '1': "At School: You are talking to a friendly teacher or a classmate about your day or a school topic.",
                '2': "At the Store: You are buying something from a helpful shopkeeper. Focus on asking for items and quantities.",
                '3': "At Home: You are talking to a kind family member (e.g., parent/sibling) about your activities or plans for the day."
            }
            initial_greetings_map = {
                '1': "Good morning! Welcome to school today. What are you working on?",
                '2': "Welcome! How can I help you today? Are you looking for anything special?",
                '3': "Hi there! What are you up to today? Anything exciting happening at home?"
            }
            
            st.session_state.roleplay_context = scenario_context_map.get(st.session_state.selected_roleplay_scenario, "")
            initial_ai_greeting_text = initial_greetings_map.get(st.session_state.selected_roleplay_scenario, "Hello!")

            # Add initial AI greeting to history and generate/play audio
            st.session_state.conversation_history.append({"role": "assistant", "content": initial_ai_greeting_text})
            try:
                response_stream = st.session_state.openai_client.audio.speech.create(
                    model="tts-1", voice="alloy", input=initial_ai_greeting_text, response_format="mp3"
                )
                initial_greeting_audio_bytes = response_stream.read()
                display_and_play_audio(initial_greeting_audio_bytes) 
                st.session_state.conversation_history[-1]["audio"] = initial_greeting_audio_bytes 
            except Exception as e:
                st.error(f"Error generating or playing initial roleplay greeting audio: {e}")

            st.rerun() # Rerun to start roleplay chat interface

# Display Conversation History (full screen width due to layout="wide")
chat_placeholder = st.container(border=True) 
 
with chat_placeholder:
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**SpeakGenie:** {message['content']}")
            if "audio" in message and message["audio"] is not None:
                st.audio(message["audio"], format="audio/mp3") 

# --- Audio Recorder for User Input ---
st.markdown("---")
# audiorecorder widget for real-time input
audio_segment = audiorecorder(
    start_prompt="Click to record", 
    stop_prompt="Stop recording",
    key="audiorecorder_widget" # Key ensures widget identity across reruns
)

# Process audio input ONLY if a new, non-empty audio segment is recorded
# This logic ensures processing happens once per unique recording
if audio_segment.frame_count() > 0: 
    current_audio_id = hash(audio_segment.raw_data) # Generate unique ID for current audio
    
    # Check if this audio segment has already been processed in the current session
    if st.session_state.last_processed_audio_id != current_audio_id:
        st.session_state.last_processed_audio_id = current_audio_id # Mark this audio as processed

        # Add "Transcribing..." placeholder to history for immediate visual feedback
        st.session_state.conversation_history.append({"role": "user", "content": "Transcribing..."})
        
        # Convert pydub AudioSegment to a temporary WAV file for Whisper
        temp_audio_path = "temp_recorded_audio.wav"
        try:
            audio_segment.export(temp_audio_path, format="wav")
        except Exception as e:
            st.error(f"Error exporting recorded audio: {e}. Ensure FFmpeg is correctly installed and accessible.")
            st.session_state.last_processed_audio_id = None # Clear ID to allow retry if export fails
            st.rerun() # Rerun to display error

        # Transcribe audio using core_tutor function
        transcribed_text = ct.transcribe_audio(st.session_state.openai_client, temp_audio_path)
        
        # Update user's last message in history with actual transcription
        # Pop the "Transcribing..." and add the actual text
        if st.session_state.conversation_history and st.session_state.conversation_history[-1]["content"] == "Transcribing...":
            st.session_state.conversation_history[-1]["content"] = transcribed_text or "Could not transcribe audio."
        else: # Fallback if Transcribing... was somehow missed (e.g., initial state)
             st.session_state.conversation_history.append({"role": "user", "content": transcribed_text or "Could not transcribe audio."})

        if transcribed_text:
            # Check for exit commands
            if ("goodbye" in transcribed_text.lower() or 
                "exit" in transcribed_text.lower() or 
                "exit roleplay" in transcribed_text.lower()):
                
                farewell_text = ""
                if st.session_state.current_mode == "Free Chat":
                    farewell_text = "Okay, goodbye for now! We can chat again anytime."
                elif st.session_state.current_mode == "Roleplay Mode":
                    farewell_text = "Okay, let's end this scenario. We can try another one, or go back to the main menu!"
                
                st.session_state.conversation_history.append({"role": "assistant", "content": farewell_text})
                
                try:
                    response_stream = st.session_state.openai_client.audio.speech.create(
                        model="tts-1", voice="alloy", input=farewell_text, response_format="mp3"
                    )
                    farewell_audio_bytes = response_stream.read()
                    display_and_play_audio(farewell_audio_bytes) # Play farewell audio immediately
                except Exception as e:
                    st.error(f"Error playing farewell audio: {e}")
                
                time.sleep(3) # Give audio time to play before rerunning

                # Reset conversation history and selected scenario on full exit
                st.session_state.conversation_history = [] 
                st.session_state.selected_roleplay_scenario = None
                st.rerun() # Rerun to go back to mode/scenario selection or clear chat
            
            # If not an exit command, get AI response
            else:
                current_roleplay_context_for_gpt = ""
                if st.session_state.current_mode == "Roleplay Mode" and st.session_state.selected_roleplay_scenario:
                    scenario_context_map = { 
                        '1': "At School: You are talking to a friendly teacher or a classmate about your day or a school topic.",
                        '2': "At the Store: You are buying something from a helpful shopkeeper. Focus on asking for items and quantities.",
                        '3': "At Home: You are talking to a kind family member (e.g., parent/sibling) about your activities or plans for the day."
                    }
                    current_roleplay_context_for_gpt = scenario_context_map.get(st.session_state.selected_roleplay_scenario, "")

                # Call handle_conversation_turn with a COPY of conversation history for LLM (excluding audio bytes)
                history_for_llm = copy.deepcopy(st.session_state.conversation_history)
                for msg in history_for_llm:
                    if "audio" in msg:
                        del msg["audio"] 

                ai_response_text, updated_history_from_ct, ai_audio_bytes = ct.handle_conversation_turn(
                    st.session_state.openai_client, 
                    transcribed_text, 
                    history_for_llm, 
                    st.session_state.current_mode.lower().replace(" ", "_"), 
                    current_roleplay_context=current_roleplay_context_for_gpt
                )
                
                # Update the actual session state history with text and potential audio for display
                st.session_state.conversation_history = updated_history_from_ct 

                if ai_response_text:
                    if ai_audio_bytes:
                        display_and_play_audio(ai_audio_bytes) # Play AI audio immediately here!
                        st.session_state.conversation_history[-1]["audio"] = ai_audio_bytes # Store audio bytes in history for replay via widget
                    else:
                        st.session_state.conversation_history[-1]["audio"] = None # Mark no audio generated
                        # Add specific message for no audio generated
                        st.session_state.conversation_history.append({"role": "assistant", "content": "I apologize, I could not generate audio for the response."}) 
                else:
                    st.session_state.conversation_history.append({"role": "assistant", "content": "I apologize, I could not generate a response."})
        else:
            # If transcription failed
            st.session_state.conversation_history.append({"role": "assistant", "content": "I apologize, I could not understand your audio. Please try again."})
        
        st.rerun() # Trigger a rerun to update the chat display and reset audiorecorder