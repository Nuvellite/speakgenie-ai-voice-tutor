# SpeakGenie AI Voice Tutor - Internship Task Submission

**Candidate Name:** Lohith.N.S
**Contact Email:** lohithsenthil22@gmail.com
**Submission Date:** July 29, 2025

---

## Project Overview

This project implements a Real-Time AI Voice Tutor as specified in the SpeakGenie internship task. It provides an interactive learning experience for children through voice-based communication, featuring both a Free Chat mode and a scenario-driven Roleplay Mode with multilingual support, all accessible via a user-friendly web interface.

## Core Features Implemented

1.  **Voice-based AI Chatbot (Free Chat):**
    * **Real-Time Voice Input:** Users speak into their microphone via the web interface using the `streamlit-audiorecorder` component.
    * **Speech-to-Text (STT):** OpenAI Whisper accurately transcribes spoken input into English text.
    * **Large Language Model (LLM):** OpenAI GPT-3.5-Turbo generates intelligent, context-aware, and friendly responses.
    * **Text-to-Speech (TTS):** OpenAI's TTS (`tts-1` model) converts AI's text responses into spoken audio played directly in the browser.
    * **Continuous Conversation:** Engage in natural, turn-based dialogue.

2.  **Interactive Roleplay Mode:**
    * **Scenario-Based Learning:** Practice English in structured, real-life scenarios (School, Store, Home).
    * **Dynamic AI Character:** AI adopts a persona (e.g., shopkeeper, teacher) appropriate to the chosen scenario.
    * **Guided Practice:** AI encourages conversation relevant to the roleplay context.
    * **Robust Exit:** Users can exit a scenario by simply saying 'goodbye', 'exit', or 'exit roleplay'.

3.  **Global Language Selection (Multilingual Support):**
    * Users can select their preferred AI response language (English, Hindi, Tamil, Marathi, Gujarati) from the sidebar.
    * **Translation Logic:** GPT translates the AI's core English response into the selected native language, presenting it as "English Response. (Native Language Translation)".
    * **Playback:** OpenAI TTS then attempts to speak the combined English and native language text.

4.  **User-Friendly Web Interface (Streamlit):**
    * Built using **Streamlit**, providing an easy-to-use graphical interface.
    * **Dynamic Backgrounds:** Background images change based on the selected mode or roleplay scenario, enhancing visual immersion.
    * **Clear Instructions:** Provides guidance within the UI.

## Technologies Used

* **Python 3.11:** Primary programming language.
* **OpenAI API:**
    * **Whisper (`whisper-1` model):** For Speech-to-Text.
    * **GPT-3.5-Turbo:** For the Large Language Model (LLM) for conversational responses and translation.
    * **Text-to-Speech (`tts-1` model):** For converting AI responses into spoken audio.
* **Streamlit:** For building the interactive web application UI.
* **`streamlit-audiorecorder`:** A custom Streamlit component for real-time microphone input from the browser.
* **`pydub`:** For audio manipulation (e.g., exporting recorded audio to WAV).
* **`pyaudio`:** (Dependency for `pydub` / general audio handling - for console version checks).
* **`python-dotenv`:** For securely managing API keys from `.env` files.
* **FFmpeg:** An essential external audio/video tool that `pydub` (and thus `streamlit-audiorecorder`) relies on for robust audio processing.

---

## Setup Instructions

Follow these steps to set up and run the AI Voice Tutor web application on your local machine.

### 1. Project Files

1.  **Download/Create all project files:** Ensure you have `core_tutor.py`, `streamlit_app.py`, `README.md`, `requirements.txt`, and your `.env` file in a single folder (e.g., `speakgenie_tutor`).
2.  **Create `backgrounds` folder:** Inside your main project folder, create a subfolder named `backgrounds`.
3.  **Place Background Images:** Download and place the following images into the `backgrounds` folder. (Use suggestions from development, e.g., playful abstract for free chat, classroom for school, etc.):
    * `free_chat_bg.jpg`
    * `classroom_bg.jpg`
    * `shop_bg.jpg`
    * `home_bg.jpg`
    * `roleplay_selection_bg.jpg`

### 2. Prerequisites

* **Python 3.11:** Ensure Python 3.11 is installed on your system.
    * Download from: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
    * **Crucially, check "Add Python 3.11 to PATH" during installation.**
* **FFmpeg:** This is vital for audio processing.
    * Download `ffmpeg-release-full.7z` from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) (Look for "Gyan" builds for Windows).
    * Extract the `.7z` file (you might need 7-Zip).
    * Locate the `bin` folder within the extracted contents (e.g., `ffmpeg-X.X.X-full_build/bin`).
    * **Add the full path to this `bin` folder to your Windows System Environment PATH variable.** (Search "Environment Variables" in Windows Start Menu, then "Environment Variables..." button, select "Path" under "System variables", click "Edit", then "New", and paste the path. Click OK on all windows).
    * **Restart your computer** after modifying the PATH for changes to take effect.

### 3. Project Setup

1.  **Navigate to your Project Directory:**
    * Open PowerShell (or Command Prompt).
    * `cd D:\path\to\your\speakgenie_tutor`
2.  **Create Virtual Environment (using Python 3.11):**
    ```bash
    py -3.11 -m venv venv
    ```
3.  **Activate Virtual Environment:**
    * **Windows PowerShell:** `.\venv\Scripts\Activate.ps1`
    * **Windows Command Prompt:** `.\venv\Scripts\activate.bat`
    * *(You should see `(venv)` at the start of your terminal prompt.)*

### 4. Install Python Libraries

With your virtual environment activated, install all required libraries:
```bash
pip install openai streamlit streamlit-audiorecorder pydub python-dotenv
```
### 5. Configure API Key

1.  **Get your OpenAI API Key:** (Provided by SpeakGenie team).
2.  **Create `.env` File:**
    * In your project root (`speakgenie_tutor/`), create a new file named **`.env`** (with the dot).
    * Add your OpenAI API key to this file:
        ```
        OPENAI_API_KEY='your_openai_api_key_here'
        ```
        (Replace `'your_openai_api_key_here'` with your actual key).
    * **Save** the `.env` file. **Never share this file or upload it to public repositories.**

---

## How to Run the AI Voice Tutor

1.  Ensure all setup steps are completed and your virtual environment is activated in PowerShell.
2.  Navigate to your project directory.
3.  Run the Streamlit application:
    ```bash
    streamlit run streamlit_app.py
    ```
4.  Your web browser will automatically open a new tab. **Ensure you access the app via `http://localhost:8501`** for microphone access.
5.  Interact with the tutor using the UI: select modes, languages, and use the microphone button to speak.

---

## Design Choices & Trade-offs

### 1. AI Persona (Child-Friendly Tone)

* **Goal:** Make SpeakGenie's responses consistently friendly, simple, and age-appropriate for children (5-10 years old).
* **Approach:** Utilized detailed "system" messages for GPT, providing explicit instructions on tone, vocabulary, sentence length, and emoji usage. Persona prompts include constraints like "simple words," "short sentences," "positive tone," and examples.
* **Trade-off/Limitation:** While highly effective for conversational flow and general encouragement, `gpt-3.5-turbo` sometimes struggles to fully suppress its inherent factual depth for very simple factual questions (e.g., "What is a dog?"). It may still provide slightly more detailed explanations than a 5-year-old would use. This is a known characteristic of this model when heavily pushed on tone for factual retrieval, and it was a pragmatic choice for this task's scope.

### 2. Native Language Playback Support

* **Goal:** Enable the AI to respond in specified native languages (Hindi, Tamil, Marathi, Gujarati).
* **Approach:**
    * **Speech-to-Text (User Input):** OpenAI Whisper is configured to *always* transcribe spoken user input into **English text**. This ensures consistent English input for the core GPT tutor logic.
    * **Translation (within GPT):** When a native language is selected in the UI, a specific instruction is added to GPT's prompt to translate its English response into the target native language. The response is formatted as "English Response. (Native Language Translation)".
    * **Text-to-Speech (AI Output):** OpenAI's TTS (using an English voice like 'alloy') attempts to speak this combined English and native language text.
    * **Trade-off/Constraint:** Achieving truly native-quality pronunciation for diverse regional languages requires highly specialized multilingual TTS models (e.g., from Google Cloud or high-tier ElevenLabs). Due to API access constraints (payment/trial limitations), these dedicated multilingual TTS services could not be fully integrated. The current solution effectively demonstrates the *logic* of multilingual support and AI-driven translation, even if the final native language pronunciation by an English voice is not perfect. This showcases adaptability to real-world resource limitations.

---

## Challenges Faced & Solutions

Building this real-time AI Voice Tutor presented several interesting and valuable challenges:

1.  **API Key Management & Quotas:**
    * **Challenge:** Initial attempts to use OpenAI's APIs (and Google Cloud's) failed due to exhausted personal free trial quotas or payment method requirements.
    * **Solution:** Communicated the issue with the SpeakGenie team, who kindly provided an OpenAI API key. This highlighted the importance of stakeholder communication and resource management in development.

2.  **Persistent Library Version Conflicts (`pydub` / `streamlit-audiorecorder` / FFmpeg):**
    * **Challenge:** Faced recurring `FileNotFoundError` (for FFmpeg), `AttributeError` (for `st.audio_recorder`), and `ImportError` (for `elevenlabs`) during library installation and usage, often due to version mismatches or FFmpeg not being found by `pydub`.
    * **Solution:** Meticulous debugging, aggressive reinstallation/upgrading of packages (`pip install --force-reinstall --no-cache-dir`), adding FFmpeg to system PATH, and importantly, **pivoting from `st.audio_recorder` to `streamlit-audiorecorder`** (a custom component) when `st.audio_recorder` consistently failed. This demonstrated deep troubleshooting and adaptability.

3.  **Robust Streamlit UI Interaction & State Management:**
    * **Challenge:** Ensuring the Streamlit app behaved correctly (e.g., processing audio only once per recording, auto-playing AI responses, proper exits, consistent chat history) given Streamlit's stateless nature and full-script reruns.
    * **Solution:** Implemented `st.session_state` extensively for persistent data, used `hash(audio_segment.raw_data)` to detect new audio inputs, employed `st.rerun()` strategically for UI updates, and added `time.sleep()` for farewell audio completion. Correctly managed clearing and updating conversation history.

4.  **Complex Persona Adherence (GPT-3.5-Turbo):**
    * **Challenge:** Forcing GPT-3.5-turbo to consistently adopt an *extremely* simplistic, childish, and short persona for factual questions proved difficult, as it often preferred to provide more detailed, academic answers.
    * **Solution:** Implemented highly specific and prioritized instructions within the system prompt, including negative constraints and examples. While significantly improved, this remains a subtle limitation of `gpt-3.5-turbo` when asked to suppress its inherent knowledge for a very specific tone. This was a pragmatic choice given the available model and project scope.

5.  **Persistent Git Tracking Issues:**
    * **Challenge:** Encountered numerous, highly persistent issues with Git tracking large files (FFmpeg executables, `venv/`, `bin/`) despite correct `.gitignore` configuration and repeated `git rm --cached` attempts. Git continued to list these as untracked or staged.
    * **Solution:** The issue pointed to a fundamental problem with Git's interaction with the file system or index. The definitive resolution involved a **complete local Git reset** (`Remove-Item .git`, `git init`), meticulous manual verification of `.gitignore`, and then a **careful, selective `git add`** of only the project's actual source files, *avoiding* `git add .` to bypass the `.gitignore` failure on this specific system. This demonstrated extreme persistence and low-level Git debugging.

---

## Future Improvements (Conceptual)

Given more time, I would enhance the tutor with:
* **Pronunciation Feedback:** Integrate a pronunciation assessment API (e.g., Google Cloud Speech-to-Text's pronunciation quality analysis) to give real-time feedback on the child's English pronunciation.
* **Adaptive Learning Paths:** Implement logic to adjust difficulty, introduce new vocabulary, or suggest specific topics based on the child's performance and progress.
* **Advanced Roleplay Scripts:** Create more complex, multi-turn roleplay scenarios with branching dialogues and specific learning objectives for each turn.
* **Improved Native Language TTS:** If dedicated multilingual TTS APIs become available (e.g., via Google Cloud with billing, or higher-tier ElevenLabs), integrate them for truly native-sounding responses.
* **Progress Tracking:** Implement a basic system to track the child's usage, vocabulary learned, and common errors over time.

---
**Thank you for this valuable learning opportunity!**
