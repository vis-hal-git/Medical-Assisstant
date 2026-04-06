import os
import logging
from datetime import datetime
from functools import wraps

from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import markdown

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

# Rate limiting to prevent abuse (using in-memory for dev, use Redis in production)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "20 per hour"],
    storage_uri="memory://"  # Explicit to suppress warning
)

# Configure OpenAI API
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    logger.warning("OPENAI_API_KEY not found in environment variables!")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Medical query categories for quick access
QUERY_CATEGORIES = {
    "symptoms": "I'm experiencing these symptoms: ",
    "medication": "Tell me about this medication: ",
    "condition": "Explain this medical condition: ",
    "prevention": "How can I prevent: ",
    "first_aid": "What is the first aid for: ",
    "nutrition": "What nutrition advice for: ",
}

# Chat history storage (in production, use a database)
chat_histories = {}


def get_session_id():
    """Get or create a session ID for chat history"""
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    return session['session_id']


def get_chat_history(session_id):
    """Retrieve chat history for a session"""
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    return chat_histories[session_id]


def add_to_history(session_id, role, content):
    """Add a message to chat history"""
    history = get_chat_history(session_id)
    history.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    # Keep only last 20 messages to manage memory
    if len(history) > 20:
        chat_histories[session_id] = history[-20:]


def create_medical_prompt(user_input, context="general"):
    """Create a structured medical prompt based on context"""
    base_prompt = """You are a knowledgeable and compassionate medical advisor. 
    Provide accurate, helpful medical information while being clear about limitations.
    
    IMPORTANT DISCLAIMERS TO INCLUDE:
    - Always recommend consulting a healthcare professional for personalized advice
    - Clarify when symptoms require urgent medical attention
    - Never diagnose conditions definitively
    
    FORMAT YOUR RESPONSE WITH:
    - Clear sections with headers when appropriate
    - Bullet points for lists of symptoms or recommendations
    - Bold text for important warnings
    - A brief summary at the end
    
    """
    
    context_prompts = {
        "general": f"""
        Medical Query: {user_input}
        
        Please provide:
        1. A clear explanation addressing the query
        2. Relevant symptoms to watch for (if applicable)
        3. General recommendations
        4. When to seek professional medical help
        """,
        
        "symptoms": f"""
        The patient reports these symptoms: {user_input}
        
        Please provide:
        1. Possible conditions these symptoms might indicate (not a diagnosis)
        2. Additional symptoms to watch for
        3. Home care recommendations
        4. Red flags that require immediate medical attention
        5. Suggested questions to ask a healthcare provider
        """,
        
        "medication": f"""
        Medication query: {user_input}
        
        Please provide:
        1. General information about the medication
        2. Common uses
        3. Typical dosage guidelines (emphasize following prescription)
        4. Common side effects
        5. Important interactions and warnings
        6. Storage recommendations
        """,
        
        "condition": f"""
        Medical condition to explain: {user_input}
        
        Please provide:
        1. What the condition is (in simple terms)
        2. Common causes and risk factors
        3. Typical symptoms
        4. How it's typically diagnosed
        5. Treatment options overview
        6. Lifestyle modifications that may help
        7. Prognosis and what to expect
        """,
        
        "prevention": f"""
        Prevention query: {user_input}
        
        Please provide:
        1. Risk factors to be aware of
        2. Lifestyle changes for prevention
        3. Dietary recommendations
        4. Exercise suggestions
        5. Screening recommendations
        6. Warning signs to watch for
        """,
        
        "first_aid": f"""
        First aid situation: {user_input}
        
        Please provide:
        1. Immediate steps to take
        2. What NOT to do
        3. When to call emergency services
        4. Follow-up care recommendations
        5. Prevention tips for the future
        """,
        
        "nutrition": f"""
        Nutrition query: {user_input}
        
        Please provide:
        1. Dietary recommendations
        2. Foods to include
        3. Foods to limit or avoid
        4. Sample meal ideas
        5. Supplements to consider (with healthcare provider approval)
        6. Hydration guidelines
        """
    }
    
    return base_prompt + context_prompts.get(context, context_prompts["general"])


def get_ai_response(prompt, temperature=0.7):
    """Get response from OpenAI API with error handling"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective model, change to "gpt-4o" for better quality
            messages=[
                {"role": "system", "content": "You are a knowledgeable and compassionate medical advisor providing accurate health information."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return f"I apologize, but I encountered an error processing your request. Please try again later. Error: {str(e)}"


def format_response_as_html(response_text):
    """Convert markdown response to HTML for better display"""
    try:
        html = markdown.markdown(
            response_text,
            extensions=['extra', 'nl2br', 'sane_lists']
        )
        return html
    except Exception:
        return response_text


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page with medical query interface"""
    session_id = get_session_id()
    chat_history = get_chat_history(session_id)
    
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()
        query_type = request.form.get('query_type', 'general')
        
        if not user_input:
            return render_template(
                'index.html',
                error="Please enter a medical query.",
                categories=QUERY_CATEGORIES,
                chat_history=chat_history
            )
        
        # Add user message to history
        add_to_history(session_id, "user", user_input)
        
        # Generate response
        prompt = create_medical_prompt(user_input, query_type)
        ai_response = get_ai_response(prompt)
        formatted_response = format_response_as_html(ai_response)
        
        # Add AI response to history
        add_to_history(session_id, "assistant", ai_response)
        
        return render_template(
            'index.html',
            user_input=user_input,
            response=formatted_response,
            raw_response=ai_response,
            query_type=query_type,
            categories=QUERY_CATEGORIES,
            chat_history=get_chat_history(session_id)
        )
    
    return render_template(
        'index.html',
        categories=QUERY_CATEGORIES,
        chat_history=chat_history
    )


@app.route('/api/query', methods=['POST'])
@limiter.limit("10 per minute")
def api_query():
    """REST API endpoint for medical queries"""
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' field"}), 400
    
    user_input = data['query'].strip()
    query_type = data.get('type', 'general')
    
    if not user_input:
        return jsonify({"error": "Query cannot be empty"}), 400
    
    prompt = create_medical_prompt(user_input, query_type)
    response = get_ai_response(prompt)
    
    return jsonify({
        "query": user_input,
        "type": query_type,
        "response": response,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear chat history for current session"""
    session_id = get_session_id()
    if session_id in chat_histories:
        chat_histories[session_id] = []
    return redirect(url_for('index'))


@app.route('/emergency')
def emergency_info():
    """Emergency information page"""
    return render_template('emergency.html')


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    return render_template(
        'index.html',
        error="Too many requests. Please wait before trying again.",
        categories=QUERY_CATEGORIES
    ), 429


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(e)}")
    return render_template(
        'index.html',
        error="An internal error occurred. Please try again later.",
        categories=QUERY_CATEGORIES
    ), 500


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)