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
    * **Branded Sidebar:** Includes a SpeakGenie logo and organized settings.
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
4.  **Place Logo Image:** Download and place `speakgenie_logo.png` (or your chosen logo image) in the project root folder.

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
