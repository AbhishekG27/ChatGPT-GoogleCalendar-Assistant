# ChatGPT Google Calendar Assistant 🗓️🤖

A powerful AI-powered calendar management system that integrates OpenAI's ChatGPT with Google Calendar, featuring voice commands through OpenAI Whisper and a sleek Streamlit interface.

## ✨ Features

- **🤖 AI-Powered Calendar Management**: Use natural language to create, modify, and manage calendar events
- **🎤 Voice Commands**: Speak to your calendar using OpenAI Whisper for speech recognition
- **📅 Google Calendar Integration**: Seamless integration with your Google Calendar
- **🔥 Firebase Backend**: Secure data storage and user authentication
- **🎨 Streamlit UI**: Beautiful and intuitive web interface
- **⚡ Real-time Processing**: Instant responses and calendar updates

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT, OpenAI Whisper
- **Calendar API**: Google Calendar API
- **Backend**: Firebase (Authentication & Database)
- **Language**: Python

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- OpenAI API key
- Firebase project

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbhishekG27/ChatGPT-GoogleCalendar-Assistant.git
   cd ChatGPT-GoogleCalendar-Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_CALENDAR_CREDENTIALS=path/to/credentials.json
   FIREBASE_CONFIG=your_firebase_config_here
   ```

4. **Configure Google Calendar API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Calendar API
   - Create credentials (OAuth 2.0 Client IDs)
   - Download the credentials file

5. **Set up Firebase**
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Authentication and Firestore Database
   - Download the Firebase configuration

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📖 Usage

### Text Commands
Simply type natural language commands like:
- "Schedule a meeting with John tomorrow at 3 PM"
- "What do I have on Friday?"
- "Cancel my 2 PM appointment"
- "Move my dentist appointment to next week"

### Voice Commands
1. Click the microphone button
2. Speak your command clearly
3. Wait for Whisper to transcribe
4. The AI will process and execute your request

## 🏗️ Project Structure

```
ChatGPT-GoogleCalendar-Assistant/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
├── src/
│   ├── calendar_manager.py    # Google Calendar integration
│   ├── openai_client.py      # OpenAI API wrapper
│   ├── firebase_client.py    # Firebase operations
│   ├── whisper_handler.py    # Voice processing
│   └── utils.py              # Utility functions
├── config/
│   └── settings.py           # Configuration settings
└── assets/
    └── images/               # UI assets
```

## 🔧 Configuration

### OpenAI Setup
1. Get your API key from [OpenAI Platform](https://platform.openai.com/)
2. Add it to your `.env` file
3. Configure the assistant model in `config/settings.py`

### Google Calendar Setup
1. Enable Google Calendar API in Google Cloud Console
2. Create OAuth 2.0 credentials
3. Download and place credentials file in your project
4. Update the path in your `.env` file

### Firebase Setup
1. Create a Firebase project
2. Enable Authentication and Firestore
3. Add your Firebase config to `.env`

## 🎯 Key Features Explained

### AI Assistant Integration
- Uses OpenAI's GPT models for natural language understanding
- Intelligent parsing of calendar-related commands
- Context-aware responses and suggestions

### Voice Recognition
- OpenAI Whisper for accurate speech-to-text conversion
- Support for multiple languages
- Real-time audio processing

### Calendar Management
- Create, read, update, delete calendar events
- Handle recurring events and reminders
- Time zone support and conflict detection

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing powerful AI models
- Google for Calendar API
- Firebase for backend services
- Streamlit for the amazing web framework

## 📧 Contact

**Abhishek G** - [2022abhishek.g@vidyashilp.edu.in] - [www.linkedin.com/in/abhishekg-1a776929b]

Project Link: [https://github.com/AbhishekG27/ChatGPT-GoogleCalendar-Assistant](https://github.com/AbhishekG27/ChatGPT-GoogleCalendar-Assistant)

---

⭐ Don't forget to star this repository if you found it helpful!
