# 🏥 Medical Advisor - AI-Powered Health Assistant

A modern Flask web application that uses OpenAI's GPT to provide medical information and health guidance.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.3+-green) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange)

## ✨ Features

- 🤖 **AI-Powered Responses** - Uses OpenAI GPT for accurate medical information
- 📂 **Multiple Query Categories** - Symptoms, Medications, Conditions, Prevention, First Aid, Nutrition
- 💬 **Chat History** - Tracks recent queries for reference
- 🎨 **Modern UI** - Beautiful, responsive design with icons and animations
- 🚨 **Emergency Page** - Quick reference for emergency situations and first aid
- 🔒 **Rate Limiting** - Protection against API abuse
- 📱 **Mobile Responsive** - Works seamlessly on all devices
- 🖨️ **Print & Copy** - Easy export of medical responses
- 🔌 **REST API** - JSON API endpoint for programmatic access

## 🖼️ Screenshots

### Main Interface
The clean, intuitive interface allows users to select query categories and get AI-powered medical advice.

### Emergency Page
Quick access to emergency information, first aid tips, and important contact numbers.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vis-hal-git/Medical-Assisstant.git
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
   # Create .env file
   copy .env.example .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=sk-your-api-key-here
   SECRET_KEY=any-random-string
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

## 📁 Project Structure

```
Medical-Assisstant/
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

## 🔧 Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Yes |
| `SECRET_KEY` | Flask session secret | Optional |
| `PORT` | Server port (default: 5000) | Optional |
| `FLASK_DEBUG` | Debug mode (default: True) | Optional |

## ⚠️ Disclaimer

**This application provides general health information only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.**

- Always consult a qualified healthcare provider for medical concerns
- Never delay seeking medical advice because of information from this tool
- Call emergency services for life-threatening situations

## 🛠️ Tech Stack

- **Backend:** Flask, Python
- **AI:** OpenAI GPT-4o-mini
- **Frontend:** HTML5, CSS3, JavaScript
- **Icons:** Font Awesome

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

**Vishal**

- GitHub: [@vis-hal-git](https://github.com/vis-hal-git)

---

⭐ Star this repo if you find it helpful!
