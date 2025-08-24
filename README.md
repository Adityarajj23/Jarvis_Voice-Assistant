# Jarvis AI Assistant

Jarvis is a simple AI-powered voice assistant built with Python.  
It can listen for a wake word ("Jarvis"), process your voice commands, and perform tasks like:
- Opening websites  
- Opening installed applications (with memory for app paths)  
- Answering general questions using Google Gemini API  

---

## Features
- **Wake word detection** ("Jarvis")
- **Voice interaction** using `speech_recognition` and `pyttsx3`
- **Open websites** by voice command
- **App manager**: remembers app paths you provide once
- **Gemini AI integration** for answering queries

---

## Setup

### 1. Clone this repo
```bash
git clone https://github.com/<your-username>/jarvis-assistant.git
cd jarvis-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API Key
In `jarvis.py`:
```python
genai.configure(api_key="YOUR_API_KEY")
```

### 4. Run Jarvis
```bash
python jarvis.py
```

---

## File Structure
```
.
├── jarvis.py        # Main assistant code
├── app_manager.py   # Handles app opening & saving paths
├── apps.json        # Stores remembered app paths
├── requirements.txt # Dependencies
└── README.md        # Documentation
```

---

## Notes
- Some apps may not be auto-detected. If so, Jarvis will ask you to provide the path manually.
- To find an app's path: right-click on its shortcut → **Properties** → copy the **Target** path.

---

## Example Usage
- Say: "Jarvis, open website YouTube"
- Say: "Jarvis, open Visual Studio Code"
- Say: "Jarvis, what is the capital of France?"

---

## License
MIT License
