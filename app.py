from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# ================= CONFIG =================

# Secret Key (Safe for Render + Local)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-123")


# Database URL Fix (Postgres + SQLite)
db_url = os.environ.get("DATABASE_URL")

if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///apis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

# Auto-create tables on startup (for Render)
with app.app_context():
    db.create_all()



# Database Table
class API(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tech = db.Column(db.String(100))
    description = db.Column(db.String(300))
    url = db.Column(db.String(200))
    code = db.Column(db.Text)
    # Rating system
    rating = db.Column(db.Integer, default=0)
    # Code generator system
    endpoint = db.Column(db.String(300))
    method = db.Column(db.String(20), default="GET")


# User Table
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="user")  # user/admin



# Home Page
@app.route("/")
def home():

    apis = API.query.all()

    user = None

    if "user_id" in session:
        user = User.query.get(session["user_id"])

    return render_template(
        "index.html",
        apis=apis,
        user=user
    )


#generator
@app.route("/generate/<int:api_id>", methods=["GET", "POST"])
def generate(api_id):
    api = API.query.get_or_404(api_id)

    if request.method == "POST":
        lang = request.form.get("language")


        if lang == "Python":
            code = f"""
import requests

url = "{api.endpoint}"

response = requests.get(url)
print(response.json())
"""

        elif lang == "JavaScript":
            code = f"""
fetch("{api.endpoint}")
    .then(res => res.json())
    .then(data => console.log(data));
"""

        elif lang == "Node.js":
            code = f"""
const axios = require("axios");

axios.get("{api.endpoint}")
    .then(res => console.log(res.data));
"""

        elif lang == "Java":
            code = f"""
        import java.net.URI;
        import java.net.http.HttpClient;
        import java.net.http.HttpRequest;
        import java.net.http.HttpResponse;

        public class Main {{
            public static void main(String[] args) throws Exception {{

                HttpClient client = HttpClient.newHttpClient();

                HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("{api.endpoint}"))
                    .build();

                HttpResponse<String> response =
                    client.send(request, HttpResponse.BodyHandlers.ofString());

                 System.out.println(response.body());
            }}
        }}
        """


        else:
            code = "No example available."

        return render_template("result.html", api=api, code=code)

    return render_template("generate.html", api=api)



# Admin Page (Protected)
@app.route("/admin", methods=["GET", "POST"])
def admin():

    # If user not logged in → send to login
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        api = API(
            name=request.form["name"],
            tech=request.form["tech"],
            description=request.form["desc"],
            url=request.form["url"],
            code=request.form["code"],
            endpoint=request.form["endpoint"]
        )

        db.session.add(api)
        db.session.commit()

        return redirect("/")

    return render_template("admin.html")


# Delete API
@app.route("/delete/<int:id>")
def delete(id):

    api = API.query.get_or_404(id)

    db.session.delete(api)
    db.session.commit()

    return redirect("/")

# ================= AUTH SYSTEM =================

# Signup
@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        hashed = generate_password_hash(request.form["password"])

        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password=hashed
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")


# Login
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        user = User.query.filter_by(
            email=request.form["email"]
        ).first()

        if user and check_password_hash(
            user.password,
            request.form["password"]
        ):

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            return redirect("/")

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


# User Profile
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    my_apis = API.query.all()  # later we link to user

    return render_template(
        "profile.html",
        user=user,
        apis=my_apis
    )

# Rate API
@app.route("/rate/<int:id>", methods=["POST"])
def rate(id):

    if "user_id" not in session:
        return redirect("/login")

    api = API.query.get_or_404(id)

    api.rating = int(request.form["rating"])

    db.session.commit()

    return redirect("/")



# Start Server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)






