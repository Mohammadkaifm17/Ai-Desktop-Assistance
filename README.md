# Jarvish AI Desktop Assistant 🎙️

Jarvish is a Python-based voice-controlled desktop assistant that listens to spoken commands and performs useful tasks such as opening websites, searching the web, retrieving weather information, announcing the date and time, playing songs through YouTube search, and capturing photos using a webcam.

## ✨ Features

- **Voice Recognition:** Recognizes spoken commands using SpeechRecognition and Google's speech recognition service.
- **Website Automation:** Opens websites such as Google, YouTube, Facebook, Spotify, and OpenAI.
- **Web Search:** Searches Google and supports searches on selected websites.
- **Weather Updates:** Retrieves current weather conditions and forecasts using WeatherAPI.
- **Music Search:** Finds songs on YouTube.
- **Date and Time:** Announces the current date and time.
- **Camera and Selfie Mode:** Captures photographs using a webcam through OpenCV.
- **Voice Responses:** Uses the macOS text-to-speech command to speak responses.

## 🛠️ Technologies Used

- Python
- SpeechRecognition
- OpenCV
- Requests
- WeatherAPI
- Google Speech Recognition
- macOS text-to-speech (`say` command)

## 📋 Prerequisites

- Python 3 installed.
- Git installed.
- A working microphone and, for selfie mode, a compatible camera.
- An internet connection for speech recognition, weather requests, and web searches.
- A WeatherAPI account and API key for weather functionality.
- macOS for the current built-in speech-output implementation.

## 🚀 Installation and Setup

### 1. Clone the repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Microphone support may require an additional audio dependency, such as PyAudio. Install a compatible version if your environment requires it.

### 4. Configure the WeatherAPI key

Obtain your own API key from [WeatherAPI](https://www.weatherapi.com/).

Set it in your terminal without adding the key to your source code:

```bash
export WEATHERAPI_KEY="YOUR_API_KEY"
```

The application must read this value using `os.getenv("WEATHERAPI_KEY")`. Never publish your real API key in the repository.

### 5. Run the assistant

Use the actual Python entry-point filename in your repository. For example, if the file is named `INDEX.PY.py`:

```bash
python INDEX.PY.py
```

Say a supported command, such as “Hello Jarvish,” “Open YouTube,” “What is the weather in Delhi?” or “Take a selfie.”

Say “Stop” to exit the assistant.

## 🔐 Permissions and Privacy

- Grant microphone access to your terminal or Python application.
- Grant camera access if you want to use selfie mode.
- Speech recognition sends audio to Google's recognition service.
- Weather requests are sent to WeatherAPI.
- Only use API keys that you are authorized to use, and keep them out of public source code.

## ⚠️ Limitations

- The current speech-output implementation uses the macOS `say` command.
- Microphone and camera features depend on local hardware, operating-system permissions, and compatible drivers.
- Internet connectivity is needed for online speech recognition and weather requests.
- Search functionality is limited to the commands implemented in the source code.
- Windows and Linux users may need changes to the speech-output and audio setup.

## 🧰 Troubleshooting

**Microphone initialization fails:** Check microphone permissions and install a compatible audio backend.

**Weather information is unavailable:** Verify your `WEATHERAPI_KEY`, internet connection, and API usage limits.

**Camera is not detected:** Check camera permissions and ensure another application is not using the camera.

**Speech is not audible:** Verify that the operating system supports the configured text-to-speech command.

**A Python module is missing:** Activate the virtual environment and reinstall dependencies from `requirements.txt`.

## 📁 Project Structure

```text
YOUR_REPOSITORY/
├── README.md
├── requirements.txt
├── .gitignore
└── INDEX.PY.py
```

Adjust the structure above to match the actual filenames in your repository.

## 📄 License

Choose and add a suitable open-source license if you want others to reuse or modify this project.

## 👨‍💻 Contributing

Contributions, bug reports, and suggestions are welcome. Please describe the issue and include the relevant steps to reproduce it.
