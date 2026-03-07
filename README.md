# ⚡ FreeAPI Dev
<div align="center">
   
![FreeAPI Dev Banner](https://img.shields.io/badge/FreeAPI-Developer%20Platform-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge\&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge\&logo=flask)
![Render](https://img.shields.io/badge/Hosted%20On-Render-46E3B7?style=for-the-badge\&logo=render)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)


**🌐 Live → [FREEAPI DEV +](https://freeapidev.onrender.com/)**

</div>

---

# 📖 Overview

**FreeAPI Dev** is a modern web platform built with **Python (Flask)** that allows developers to explore, test, and experiment with free APIs.

The project demonstrates:

* Backend web development
* API architecture
* Flask application structure
* Cloud deployment
* Production configuration using **WSGI + Gunicorn**

This platform acts as a **developer API directory and testing environment**, helping developers quickly find APIs for their projects.

---

# ✨ Key Features

### 🔌 API Directory

Browse a collection of free APIs categorized by type.

### 🐍 Python Flask Backend

Lightweight backend using the Flask framework.

### 📄 Dynamic HTML Rendering

Uses **Jinja2 templates** for server-side rendering.

### 🚀 Production Ready

Configured with **WSGI + Gunicorn** for scalable deployment.

### ☁️ Cloud Deployment

Hosted on **Render Cloud Platform**.

### ⚡ Fast & Lightweight

Minimal dependencies and optimized architecture.

### 🧩 Modular Codebase

Clean and organized project structure.

---

# 🛠️ Technologies Used

| Technology   | Purpose                |
| ------------ | ---------------------- |
| **Python**   | Backend programming    |
| **Flask**    | Web framework          |
| **Jinja2**   | HTML templating        |
| **Gunicorn** | Production WSGI server |
| **Render**   | Cloud hosting          |
| **HTML/CSS** | Frontend UI            |

---

# 📂 Project Structure

```
freeapidev/
│
├── templates/          # HTML templates
│
├── app.py              # Main Flask application
│
├── wsgi.py             # Production entry point
│
├── requirements.txt    # Python dependencies
│
├── README.md           # Project documentation
│
└── LICENSE             # MIT License
```

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/KanavChauhan23/freeapidev.git
cd freeapidev
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run the Application

```bash
python app.py
```

OR

```bash
flask run
```

---

## 5️⃣ Open in Browser

```
http://localhost:5000
```

---

# ⚙️ Production Deployment

Run using **Gunicorn WSGI server**:

```bash
gunicorn wsgi:app
```

---

# 🌍 Deploying to Render

1️⃣ Fork the repository

2️⃣ Create a **Web Service** on Render

3️⃣ Configure:

Build Command

```
pip install -r requirements.txt
```

Start Command

```
gunicorn wsgi:app
```

4️⃣ Deploy

Your application will be available at:

```
https://your-app-name.onrender.com
```

---

# 📡 Example API Routes

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| GET    | `/`              | Homepage              |
| GET    | `/api`           | API information       |
| POST   | `/api/data`      | Submit data           |
| GET    | `/api/data/<id>` | Fetch specific record |

---

# 🔒 Security Best Practices

* Store sensitive values in **environment variables**
* Never commit `.env` files
* Enable **HTTPS in production**
* Validate user inputs
* Implement rate limiting for APIs

---

# 🧪 Testing

Run tests using:

```bash
pytest
```

---

# 🌐 Browser Support

✔ Chrome
✔ Firefox
✔ Edge
✔ Safari

---

# 🤝 Contributing

Contributions are welcome!

Steps:

1️⃣ Fork the repository
2️⃣ Create a feature branch

```bash
git checkout -b feature/new-feature
```

3️⃣ Commit changes

```bash
git commit -m "Added new feature"
```

4️⃣ Push to GitHub

```bash
git push origin feature/new-feature
```

5️⃣ Create Pull Request

---

# 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

# 👨‍💻 Author

**Kanav Chauhan**
- Portfolio: [kanavportfolio.vercel.app](https://kanavportfolio.vercel.app)
- GitHub: [@KanavChauhan](https://github.com/KanavChauhan)

---

# 🛣️ Future Roadmap

Planned improvements:

* 🔐 User Authentication
* 📊 API Dashboard
* ⭐ Favorite APIs
* 🔍 Advanced Search
* ⚡ API Testing Tool
* 🧠 AI API Recommendations
* 📈 API Usage Analytics
* 🌙 Dark / Light Mode

---

# ⭐ Support

If you like this project:

⭐ **Star the repository**
🍴 **Fork the project**
📢 **Share with developers**

---

**Made with ❤️ by Kanav Chauhan**
