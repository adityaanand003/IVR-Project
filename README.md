# 📞 Plivo IVR System

A multilingual Interactive Voice Response (IVR) system built with Flask and Plivo that provides automated phone menu functionality in English and Spanish.

## 🌟 Features

- **Multilingual Support**: English and Spanish language options
- **3-Level Menu System**: 
  - Level 1: Language selection
  - Level 2: Action selection  
  - Level 3: Final actions (audio message or connect to associate)
- **DTMF Input Handling**: Reliable touch-tone key detection
- **Live Call Transfer**: Connect callers to human associates
- **Debug Endpoints**: Built-in testing and debugging tools
- **Error Handling**: Graceful fallbacks for invalid inputs

## 📋 Call Flow

```
📱 Call Initiated
    ↓
🌍 "Welcome to Inspire Works. Press 1 for English, Press 2 for Spanish"
    ↓
┌─────────────────┬─────────────────┐
│   English (1)   │   Spanish (2)   │
└─────────────────┴─────────────────┘
    ↓                       ↓
📋 "Press 1 for audio      📋 "Presione 1 para mensaje
   message, Press 2           de audio, Presione 2
   to speak to associate"     para hablar con asociado"
    ↓                       ↓
┌──────────────┬──────────────────┐
│ Audio Msg(1) │ Connect Agent(2) │
└──────────────┴──────────────────┘
    ↓               ↓
🎵 Play Message   📞 Transfer Call
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Flask
- Plivo Python SDK
- ngrok (for local development)
- Active Plivo account

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd plivo-ivr-system
   ```

2. **Install dependencies**
   ```bash
   pip install flask plivo
   ```

3. **Configure your settings**
   
   **In `trigger.py`:**
   ```python
   AUTH_ID = "YOUR_PLIVO_AUTH_ID"
   AUTH_TOKEN = "YOUR_PLIVO_AUTH_TOKEN"
   SOURCE_NUMBER = "YOUR_PLIVO_PHONE_NUMBER"
   DESTINATION_NUMBER = "YOUR_TEST_PHONE_NUMBER"
   NGROK_URL = "YOUR_NGROK_URL"
   ```

   **In `app.py`:**
   ```python
   ASSOCIATE_NUMBER = "PHONE_NUMBER_TO_TRANSFER_CALLS"
   NGROK_URL = "YOUR_NGROK_URL"
   ```

4. **Start the Flask application**
   ```bash
   python app.py
   ```

5. **Start ngrok tunnel** (in separate terminal)
   ```bash
   ngrok http 5000
   ```

6. **Update ngrok URL** in both files with the generated URL

7. **Test the system**
   ```bash
   python trigger.py
   ```

## 📁 File Structure

```
plivo-ivr-system/
├── app.py          # Main Flask application with IVR logic
├── trigger.py      # Call initiation script
└── README.md       # This file
```

## 🔧 Configuration

### Plivo Setup

1. Sign up for a [Plivo account](https://www.plivo.com/)
2. Get your `AUTH_ID` and `AUTH_TOKEN` from the dashboard
3. Purchase/rent a phone number for the `SOURCE_NUMBER`
4. Update the configuration in `trigger.py`

### ngrok Setup

1. Install ngrok from [ngrok.com](https://ngrok.com/)
2. Get your authtoken and configure it
3. Start tunnel: `ngrok http 5000`
4. Copy the generated HTTPS URL to both files

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ivr` | GET/POST | Main IVR entry point (language selection) |
| `/ivr/level2` | POST | Action selection based on language |
| `/ivr/action` | POST | Final action execution |
| `/debug` | GET/POST | Test ngrok connectivity |
| `/test-xml` | GET | View generated XML structure |

## 🔍 Debug Features

- **Debug logging**: Console output for tracking call flow
- **Test endpoints**: `/debug` and `/test-xml` for troubleshooting
- **Error handling**: Graceful fallbacks for invalid inputs
- **XML validation**: Manual XML generation for reliable DTMF handling

## 📞 Usage Examples

### Making a Test Call
```bash
python trigger.py
```

### Testing Connectivity
Visit: `https://your-ngrok-url.ngrok-free.app/debug`

### Viewing XML Structure
Visit: `https://your-ngrok-url.ngrok-free.app/test-xml`

## 🌐 Language Support

- **English**: Full IVR flow with US English pronunciation
- **Spanish**: Complete Spanish translation with ES Spanish pronunciation
- **Extensible**: Easy to add more languages by modifying Level 2 logic

## ⚙️ Technical Details

### XML Structure Fix
The system uses manually crafted XML instead of the Plivo SDK to ensure proper `<Speak>` element nesting within `<GetDigits>`, which resolves DTMF input capture issues.

### DTMF Configuration
- **Timeout**: 15 seconds for input
- **Finish Key**: `#` (optional)
- **Single Digit**: Captures one keypress per level

### Error Handling
- Invalid language selection → Return to main menu
- Invalid action selection → Return to main menu  
- No input received → Timeout message and hangup
- Invalid final input → "Invalid input" message

## 🚨 Troubleshooting

### Common Issues

1. **DTMF not working**
   - Ensure XML has proper `<Speak>` nesting inside `<GetDigits>`
   - Check ngrok tunnel is active and accessible

2. **Calls not connecting**
   - Verify Plivo credentials are correct
   - Check phone number format (include country code)
   - Ensure ngrok URL is updated in both files

3. **"No input received"**
   - Hold keys longer (1-2 seconds)
   - Try different phone/device
   - Check network connectivity

4. **Associate transfer fails**
   - Verify `ASSOCIATE_NUMBER` format
   - Ensure destination number can receive calls

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ using Flask, Plivo, and Python**
