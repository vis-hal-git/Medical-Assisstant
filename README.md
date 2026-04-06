# Medical Advisor - AI-Powered Health Assistant

A modern Flask web application that uses Google's Gemini AI to provide medical information and health guidance. Features a beautiful, responsive UI with multiple query categories and chat history.

![Medical Advisor](https://img.shields.io/badge/AI-Gemini%202.0-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![Flask](https://img.shields.io/badge/Flask-2.3+-orange)

## ✨ Features

- **🤖 AI-Powered Responses**: Leverages Google's Gemini 2.0 Flash for accurate medical information
- **📂 Multiple Query Categories**: Symptoms, Medications, Conditions, Prevention, First Aid, Nutrition
- **💬 Chat History**: Keeps track of recent queries for reference
- **🎨 Modern UI**: Beautiful, responsive design with icons and animations
- **🚨 Emergency Page**: Quick reference for emergency situations and first aid
- **🔒 Rate Limiting**: Protection against API abuse
- **📱 Mobile Responsive**: Works seamlessly on all devices
- **🖨️ Print & Copy**: Easy export of medical responses
- **🔌 REST API**: JSON API endpoint for programmatic access

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KalyanMurapaka45/Medical-Assisstant.git
   cd Medical-Assisstant
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   GEMINI_API_KEY=your_actual_api_key
   SECRET_KEY=your_secret_key
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open your browser:**
   Navigate to [http://localhost:5000](http://localhost:5000)

## 📖 Usage

### Web Interface

1. Select a query category (Symptoms, Medication, Condition, etc.)
2. Enter your medical question in the text area
3. Click "Get Medical Advice" for AI-generated response
4. Use quick prompts for common query types
5. Copy or print responses as needed

### REST API

```bash
# POST /api/query
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are symptoms of diabetes?", "type": "condition"}'
```

**Response:**
```json
{
  "query": "What are symptoms of diabetes?",
  "type": "condition",
  "response": "...",
  "timestamp": "2024-01-15T10:30:00"
}
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET/POST | Main web interface |
| `/api/query` | POST | REST API for queries |
| `/emergency` | GET | Emergency information |
| `/clear-history` | POST | Clear chat history |
| `/health` | GET | Health check endpoint |

## 🏗️ Project Structure

```
Medical-Assistant/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── static/
│   └── style.css       # Modern CSS styles
├── templates/
│   ├── index.html      # Main interface
│   └── emergency.html  # Emergency info page
└── README.md
```

## ⚠️ Disclaimer

**This application provides general health information only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.**

- Always consult a qualified healthcare provider for medical concerns
- Never delay seeking medical advice because of information from this tool
- Call emergency services for life-threatening situations

## 🔧 Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `SECRET_KEY` | Flask session secret | Random |
| `PORT` | Server port | 5000 |
| `FLASK_DEBUG` | Debug mode | True |

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Kalyan Murapaka - [kalyanmurapaka274@gmail.com](mailto:kalyanmurapaka274@gmail.com)

Project Link: [https://github.com/KalyanMurapaka45/Medical-Assisstant](https://github.com/KalyanMurapaka45/Medical-Assisstant)
