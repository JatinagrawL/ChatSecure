# #GPT - Secure LLM Wrapper

## Overview

#GPT is a Flask-based web application that serves as a secure wrapper for various Large Language Model (LLM) APIs, with built-in Personally Identifiable Information (PII) detection and redaction capabilities. The application provides a chat interface that automatically detects and redacts sensitive information before sending messages to LLM providers like OpenAI and Anthropic.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple three-tier architecture:

1. **Presentation Layer**: Flask templates with Bootstrap-based responsive UI
2. **Application Layer**: Flask web server with session-based state management
3. **Integration Layer**: HTTP clients for external LLM API communication

The architecture prioritizes simplicity and security, with PII detection occurring at the application layer before any external API calls.

## Key Components

### Core Application (`app.py`)
- **Flask Web Server**: Main application entry point with route handlers
- **Session Management**: Stores API configuration and chat history in server-side sessions
- **API Configuration**: Handles setup and validation of different LLM providers
- **Request Routing**: Manages user interactions and API calls

### PII Detection Engine (`pii_detector.py`)
- **Pattern Matching**: Uses regex patterns to identify common PII types (emails, phones, SSNs, addresses)
- **Name Detection**: Maintains dictionaries of common first and last names for identification
- **Redaction Logic**: Replaces detected PII with generic placeholders
- **Multiple PII Types**: Supports detection of emails, phone numbers, social security numbers, dates of birth, addresses, and zip codes

### LLM Client (`llm_client.py`)
- **Multi-Provider Support**: Unified interface for OpenAI, Anthropic, and custom APIs
- **Authentication Handling**: Provider-specific header and authentication management
- **Connection Testing**: Validates API connectivity before enabling chat functionality
- **Request Formatting**: Adapts message formats to each provider's API requirements

### Frontend Components
- **Bootstrap UI**: Responsive design with dark theme optimized for chat interactions
- **Real-time Chat**: JavaScript-powered chat interface with typing indicators and message streaming
- **Configuration Interface**: User-friendly setup for API providers and credentials

## Data Flow

1. **Configuration Phase**:
   - User selects LLM provider and enters API credentials
   - Application validates connection and stores configuration in session
   - Redirects to chat interface upon successful validation

2. **Chat Interaction**:
   - User submits message through web interface
   - PII detector scans message and creates redacted version
   - LLM client sends redacted message to configured API
   - Response is received and displayed to user
   - Original and redacted messages stored in session history

3. **PII Protection Flow**:
   - Text input → Pattern matching → Name detection → Redaction → External API call
   - Redaction information tracked and displayed to user for transparency

## External Dependencies

### Required APIs
- **OpenAI API**: For GPT-3.5/GPT-4 models (endpoint: https://api.openai.com/v1/chat/completions)
- **Anthropic API**: For Claude models (endpoint: https://api.anthropic.com/v1/messages)
- **Google Gemini API**: For Gemini models (endpoint: https://generativelanguage.googleapis.com/v1beta/models)
- **DeepSeek API**: For DeepSeek models (endpoint: https://api.deepseek.com/v1/chat/completions)
- **xAI Grok API**: For Grok models (endpoint: https://api.x.ai/v1/chat/completions)

### Python Dependencies
- **Flask**: Web framework for application structure and routing
- **Requests**: HTTP client library for API communications
- **Logging**: Built-in Python logging for debugging and monitoring

### Frontend Dependencies
- **Bootstrap 5.3.0**: CSS framework for responsive UI components
- **Font Awesome 6.4.0**: Icon library for user interface elements
- **Vanilla JavaScript**: Client-side functionality without additional frameworks

## Deployment Strategy

### Development Environment
- **Local Development**: Flask development server with debug mode enabled
- **Port Configuration**: Runs on port 5000 with host binding to 0.0.0.0
- **Session Management**: Uses environment variable for session secret or falls back to development key

### Security Considerations
- **No Persistent Storage**: All data stored in server-side sessions (memory-based)
- **API Key Protection**: Credentials stored only in session, not logged or persisted
- **PII Redaction**: Automatic detection and replacement before external API calls
- **HTTPS Recommendation**: Should be deployed behind HTTPS proxy in production

### Scalability Limitations
- **Session-Based Architecture**: Limited to single-server deployments without session store
- **Memory Storage**: Chat history and configuration lost on server restart
- **No Database Layer**: Intentional design choice for simplicity and security

### Production Recommendations
- Set `SESSION_SECRET` environment variable to secure random value
- Deploy behind reverse proxy (nginx/Apache) with HTTPS
- Consider implementing rate limiting for API calls
- Add proper logging and monitoring for production use
- Implement session persistence if multi-server deployment needed

The application is designed for simplicity and security over scalability, making it ideal for personal use or small team deployments where PII protection is paramount.