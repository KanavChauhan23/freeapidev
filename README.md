# FreeAPI Dev

![FreeAPI Dev Banner](https://img.shields.io/badge/FreeAPI-Dev%20Platform-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-black?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render)

## 🌐 Live Demo

**[🚀 Visit Live Application](https://freeapidev.onrender.com/)**

## 📋 Overview

FreeAPI Dev is a Python-based web application built with Flask/WSGI that provides a platform for free API development and testing. This project demonstrates backend development skills, API architecture, and deployment capabilities on modern cloud platforms.

## ✨ Features

- 🔌 **RESTful API Endpoints** - Clean and well-structured API architecture
- 🐍 **Python Backend** - Powered by Flask framework
- 📄 **Template System** - Dynamic HTML rendering with Jinja2
- 🚀 **Production Ready** - Configured with WSGI for production deployment
- ☁️ **Cloud Deployed** - Live on Render platform
- 📦 **Modular Structure** - Organized templates and application logic
- ⚡ **Fast & Lightweight** - Optimized for performance

## 🛠️ Technologies Used

- **Python** (34.2%) - Backend logic and API development
- **HTML/Jinja2** (65.8%) - Frontend templates and rendering
- **Flask** - Web framework
- **WSGI** - Production server interface
- **Render** - Cloud hosting platform

## 📂 Project Structure

```
freeapidev/
│
├── templates/          # HTML templates for web pages
├── app.py             # Main Flask application
├── wsgi.py            # WSGI entry point for production
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
└── LICENSE            # MIT License file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KanavChauhan23/freeapidev.git
   cd freeapidev
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   # Development mode
   python app.py

   # Or using Flask CLI
   flask run
   ```

5. **Access the application:**
   - Open your browser and navigate to `http://localhost:5000`

### Production Deployment

For production deployment using WSGI:
```bash
gunicorn wsgi:app
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:
```env
FLASK_APP=app.py
FLASK_ENV=development  # Change to 'production' for production
SECRET_KEY=your-secret-key-here
PORT=5000
```

### Requirements

All dependencies are listed in `requirements.txt`. Key packages include:
- Flask
- Gunicorn (for production)
- Additional packages as needed

## 📡 API Endpoints

> Document your API endpoints here

Example:
```
GET  /api/           - Get API information
POST /api/data       - Submit data
GET  /api/data/:id   - Retrieve specific data
```

## 🌟 Deployment

### Deploy to Render

1. **Fork this repository** to your GitHub account

2. **Create a new Web Service** on [Render](https://render.com)

3. **Connect your repository** and configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Environment:** Python 3

4. **Deploy!** Your app will be live at `https://your-app-name.onrender.com`

### Deploy to Other Platforms

- **Heroku:** Use `Procfile` with `web: gunicorn wsgi:app`
- **Railway:** Connect repository and deploy automatically
- **PythonAnywhere:** Upload files and configure WSGI
- **AWS/GCP/Azure:** Use containerization with Docker

## 🔒 Security

- Always use environment variables for sensitive data
- Never commit `.env` files or API keys
- Implement rate limiting for production APIs
- Use HTTPS in production
- Validate and sanitize all user inputs

## 🧪 Testing

Run tests with:
```bash
# If you have tests configured
pytest

# Or run specific test file
python -m pytest tests/
```

## 📱 Browser Compatibility

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write docstrings for functions and classes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Kanav Chauhan**
- GitHub: [@KanavChauhan23](https://github.com/KanavChauhan23)
- Live Demo: [FreeAPI Dev](https://freeapidev.onrender.com/)

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Deployed on [Render](https://render.com/)
- Thanks to the Python and Flask community

## 📧 Support

For support, issues, or questions:
- Open an issue on [GitHub Issues](https://github.com/KanavChauhan23/freeapidev/issues)
- Contact through the live application

## 🔮 Roadmap

- [ ] Add user authentication
- [ ] Implement database integration
- [ ] Add more API endpoints
- [ ] Create comprehensive API documentation
- [ ] Add rate limiting
- [ ] Implement caching
- [ ] Add automated testing
- [ ] Create API dashboard

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/KanavChauhan23/freeapidev?style=social)
![GitHub forks](https://img.shields.io/github/forks/KanavChauhan23/freeapidev?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/KanavChauhan23/freeapidev?style=social)

---

⭐ If you find this project useful, please consider giving it a star!

**Made with ❤️ by Kanav Chauhan**
