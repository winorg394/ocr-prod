I'll update the README.md to be more GitHub-friendly with additional sections and badges. Here's the updated version:

```markdown:c:\Users\User\Desktop\projet\vscode-projet\ocr\ocr\README.md
# Flight Ticket OCR API 🎫

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-blue.svg)](https://openai.com/)

An intelligent OCR system that extracts structured information from flight tickets using AI and machine learning.

## 🚀 Features

- 📝 Extract text from images using EasyOCR
- 📄 Process PDF documents with PyMuPDF
- 🤖 AI-powered text processing via OpenRouter API
- 🔄 Support for multiple file formats (PDF, JPG, PNG)
- ⚙️ Customizable AI model selection
- 🌐 RESTful API interface
- 🔒 Secure file handling

## 🛠️ Tech Stack

- Python 3.8+
- Flask (Web Framework)
- EasyOCR (Optical Character Recognition)
- PyMuPDF (PDF Processing)
- OpenAI API (Text Processing)
- OpenRouter API (Model Selection)

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/Lugginteam/luggin-flight-ocr-api.git
cd luggin-flight-ocr-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
# Create a .env file and add your API keys
OPENROUTER_API_KEY=your_api_key_here
```

## 🚀 Quick Start

1. Start the API server:
```bash
python ocr/api.py
```

2. Process a ticket:
```bash
python ocr/ocr.py path/to/ticket.pdf
```

## 🔍 API Endpoints

### Extract Ticket Information
```http
POST /api/extract
Content-Type: multipart/form-data

file: <ticket_file>
model: <ai_model_name> (optional)
```

### Supported Models
- DeepSeek Chat (default)
- Claude 3 Haiku
- Claude 3 Sonnet
- Llama 3 8B

## 📤 Output Format

```json
{
  "airline": "string",
  "flight_number": "string",
  "passenger_name": "string",
  "departure_airport": "string",
  "arrival_airport": "string",
  "departure_date": "YYYY-MM-DD",
  "departure_time": "HH:MM",
  "arrival_date": "YYYY-MM-DD",
  "arrival_time": "HH:MM",
  "seat_number": "string",
  "booking_reference": "string",
  "ticket_number": "string",
  "fare_class": "string",
  "baggage_allowance": "string"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Luggin Team** - *Initial work*

## 🙏 Acknowledgments

- EasyOCR team for the OCR engine
- OpenAI for the text processing capabilities
- OpenRouter for model access
- Flask team for the web framework

## 📞 Support

For support, email support@luggin.com or create an issue in the repository.
```

This updated README includes:
1. Badges for quick information
2. Emojis for better visual organization
3. Detailed API documentation
4. Contributing guidelines
5. Support information
6. Better formatting and structure
7. Tech stack details
8. Prerequisites section
9. JSON output format example
10. Authors and acknowledgments sections#   o c r - p r o d  
 