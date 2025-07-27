# #GPT - Secure LLM Wrapper

A Flask-based web application that serves as a secure wrapper for various Large Language Model APIs, with built-in PII detection and synthetic replacement capabilities.

## Features

- 🛡️ **Automatic PII Protection**: Detects and replaces personal information with synthetic values
- 🤖 **Multiple AI Providers**: Supports OpenAI, Anthropic, Google Gemini, DeepSeek, and xAI Grok
- 🎨 **Modern UI**: Dark theme with glassmorphism effects and responsive design
- 💬 **Real-time Chat**: Interactive chat interface with typing indicators
- 🔒 **Session-based Security**: No persistent storage of sensitive data

## Running in Visual Studio Code

### Prerequisites

Make sure you have Python 3.11+ installed on your system.

### Setup Steps

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd gpt-secure-wrapper
   ```

2. **Open in Visual Studio Code**
   ```bash
   code .
   ```

3. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   ```

4. **Activate Virtual Environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

5. **Install Dependencies**
   ```bash
   pip install flask requests gunicorn
   ```

6. **Set Environment Variables** (Optional)
   Create a `.env` file in the project root:
   ```
   SESSION_SECRET=your-secret-key-here
   ```

7. **Run the Application**
   
   **Option 1: Using Flask (Development)**
   ```bash
   python app.py
   ```
   
   **Option 2: Using Gunicorn (Production-like)**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reload main:app
   ```

8. **Access the Application**
   Open your browser and go to: `http://localhost:5000`

### VS Code Setup Tips

1. **Install Python Extension**
   - Install the "Python" extension by Microsoft for better Python support

2. **Select Python Interpreter**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Python: Select Interpreter"
   - Choose the interpreter from your virtual environment

3. **Debugging Setup**
   Create `.vscode/launch.json`:
   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python: Flask",
               "type": "python",
               "request": "launch",
               "program": "app.py",
               "env": {
                   "FLASK_ENV": "development"
               },
               "console": "integratedTerminal"
           }
       ]
   }
   ```

4. **Terminal in VS Code**
   - Use `Ctrl+`` (backtick) to open integrated terminal
   - Run commands directly in VS Code terminal

### API Keys Setup

1. **Get API Keys** from your chosen provider:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Google Gemini: https://aistudio.google.com/app/apikey
   - DeepSeek: https://platform.deepseek.com/api_keys
   - xAI Grok: https://console.x.ai/

2. **Configure in Application**
   - Select your AI provider from the dropdown
   - Enter your API key
   - Click "Connect & Test API"

### File Structure

```
├── app.py              # Main Flask application
├── main.py             # Entry point for Gunicorn
├── pii_detector.py     # PII detection and replacement logic
├── llm_client.py       # LLM API client implementations
├── templates/          # HTML templates
│   ├── index.html      # Configuration page
│   └── chat.html       # Chat interface
├── static/             # CSS and JavaScript files
│   ├── css/style.css   # Styling
│   └── js/chat.js      # Chat functionality
└── replit.md           # Project documentation
```

### Troubleshooting

**Port Already in Use:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Module Not Found:**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**API Connection Issues:**
- Verify your API key is correct
- Check your internet connection
- Ensure the API service is not experiencing outages

### Development

To modify the application:
- **Backend**: Edit `app.py`, `pii_detector.py`, or `llm_client.py`
- **Frontend**: Edit files in `templates/` and `static/`
- **Styling**: Modify `static/css/style.css`
- **JavaScript**: Edit `static/js/chat.js`

The application will automatically reload when you make changes (if using `--reload` flag with Gunicorn or Flask development mode).