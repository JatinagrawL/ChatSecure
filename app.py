import os
import logging
from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
from pii_detector import PIIDetector
from llm_client import LLMClient

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize PII detector
pii_detector = PIIDetector()

@app.route('/')
def index():
    """Main page for API configuration"""
    return render_template('index.html')

@app.route('/configure', methods=['POST'])
def configure_api():
    """Configure LLM API settings"""
    api_key = request.form.get('api_key', '').strip()
    api_provider = request.form.get('api_provider', 'openai')
    
    if not api_key:
        flash('API key is required', 'error')
        return redirect(url_for('index'))
    
    # Set default endpoints based on provider
    endpoint_map = {
        'openai': 'https://api.openai.com/v1/chat/completions',
        'anthropic': 'https://api.anthropic.com/v1/messages',
        'gemini': 'https://generativelanguage.googleapis.com/v1beta/models',
        'deepseek': 'https://api.deepseek.com/v1/chat/completions',
        'grok': 'https://api.x.ai/v1/chat/completions'
    }
    
    api_endpoint = endpoint_map.get(api_provider)
    if not api_endpoint:
        flash('Unsupported API provider', 'error')
        return redirect(url_for('index'))
    
    # Store in session
    session['api_key'] = api_key
    session['api_endpoint'] = api_endpoint
    session['api_provider'] = api_provider
    session['chat_history'] = []
    
    # Test API connection
    llm_client = LLMClient(api_key, api_endpoint, api_provider)
    if not llm_client.test_connection():
        flash('Failed to connect to API. Please check your credentials.', 'error')
        return redirect(url_for('index'))
    
    flash('API configured successfully!', 'success')
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    """Chat interface"""
    if 'api_key' not in session:
        flash('Please configure your API first', 'error')
        return redirect(url_for('index'))
    
    return render_template('chat.html', 
                         chat_history=session.get('chat_history', []),
                         api_provider=session.get('api_provider', 'openai'))

@app.route('/send_message', methods=['POST'])
def send_message():
    """Process and send message to LLM"""
    if 'api_key' not in session:
        return jsonify({'error': 'API not configured'}), 400
    
    data = request.get_json()
    user_message = data.get('message', '').strip() if data else ''
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    try:
        # Detect and redact PII
        redacted_message, redactions = pii_detector.redact_pii(user_message)
        
        # Initialize LLM client
        llm_client = LLMClient(
            session['api_key'], 
            session['api_endpoint'], 
            session['api_provider']
        )
        
        # Send redacted message to LLM
        response = llm_client.send_message(redacted_message)
        
        if response is None:
            return jsonify({'error': 'Failed to get response from LLM API'}), 500
        
        # Store in chat history
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        session['chat_history'].append({
            'user_message': user_message,
            'redacted_message': redacted_message,
            'redactions': redactions,
            'assistant_response': response
        })
        session.modified = True
        
        return jsonify({
            'success': True,
            'user_message': user_message,
            'redacted_message': redacted_message,
            'redactions': redactions,
            'assistant_response': response
        })
        
    except Exception as e:
        app.logger.error(f"Error processing message: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your message'}), 500

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    """Clear chat history"""
    session['chat_history'] = []
    session.modified = True
    return jsonify({'success': True})

@app.route('/disconnect')
def disconnect():
    """Disconnect from API and clear session"""
    session.clear()
    flash('Disconnected successfully', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
