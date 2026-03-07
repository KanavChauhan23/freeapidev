# ─────────────────────────────────────────────────────────────────
#  app.py  —  DevAPI Hub  (complete, all routes working)
# ─────────────────────────────────────────────────────────────────
from flask import (Flask, render_template, request,
                   redirect, url_for, session, flash)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests, os

app = Flask(__name__)

# ── Config ────────────────────────────────────────────────────────
app.secret_key = os.environ.get("SECRET_KEY", "devapiHub_secret_2025")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///devapiHub.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ── DB Models ─────────────────────────────────────────────────────
class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),  unique=True,  nullable=False)
    email    = db.Column(db.String(120), unique=True,  nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role     = db.Column(db.String(20),  default="user")
    apis     = db.relationship("API", backref="author", lazy=True)


class API(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    tech        = db.Column(db.String(50),  nullable=False)
    description = db.Column(db.String(300), nullable=False)
    url         = db.Column(db.String(300), nullable=False)
    code        = db.Column(db.Text,        nullable=False)
    endpoint    = db.Column(db.String(300), nullable=False)
    method      = db.Column(db.String(10),  default="GET")
    user_id     = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)


# ── 100 Embedded Public APIs (fallback when live source is down) ──
EMBEDDED_APIS = [
    {"API":"Cat Facts","Description":"Random cat facts and trivia for any app","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://catfact.ninja/","Category":"Animals"},
    {"API":"Dog CEO","Description":"Random dog breed images from 115+ breeds","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://dog.ceo/dog-api/","Category":"Animals"},
    {"API":"RandomFox","Description":"Random fox photographs via simple REST API","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://randomfox.ca/","Category":"Animals"},
    {"API":"The Cat API","Description":"Cat images, breeds and facts with voting system","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://thecatapi.com/","Category":"Animals"},
    {"API":"Zoo Animals","Description":"Random zoo animal facts and information","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://zoo-animal-api.herokuapp.com/","Category":"Animals"},
    {"API":"HTTP Cat","Description":"Cat image for every HTTP status code","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://http.cat/","Category":"Animals"},
    {"API":"PokéAPI","Description":"All Pokémon data — species, moves, abilities","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://pokeapi.co/","Category":"Animals"},
    {"API":"iNaturalist","Description":"Citizen science biodiversity observations","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://www.inaturalist.org/","Category":"Animals"},
    {"API":"OpenAI","Description":"GPT-4, DALL-E, Whisper and embeddings API","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://platform.openai.com/","Category":"AI"},
    {"API":"Hugging Face","Description":"300,000+ ML models via inference API","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://huggingface.co/","Category":"AI"},
    {"API":"Cohere","Description":"LLMs for generation, classification and embedding","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://cohere.com/","Category":"AI"},
    {"API":"Stability AI","Description":"Stable Diffusion image generation APIs","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://platform.stability.ai/","Category":"AI"},
    {"API":"AssemblyAI","Description":"Speech recognition and audio intelligence","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://www.assemblyai.com/","Category":"AI"},
    {"API":"Replicate","Description":"Run open-source ML models in the cloud","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://replicate.com/","Category":"AI"},
    {"API":"DeepSeek","Description":"Open-source code and reasoning AI models","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://platform.deepseek.com/","Category":"AI"},
    {"API":"Groq","Description":"Ultra-fast LLM inference with custom LPU hardware","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://console.groq.com/","Category":"AI"},
    {"API":"ElevenLabs","Description":"AI voice generation and ultra-realistic cloning","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://elevenlabs.io/","Category":"AI"},
    {"API":"Mistral AI","Description":"Open portable generative AI models","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://docs.mistral.ai/","Category":"AI"},
    {"API":"OpenWeatherMap","Description":"Current weather, forecasts and historical data","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://openweathermap.org/api","Category":"Weather"},
    {"API":"WeatherAPI","Description":"Real-time forecasts with air quality data","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://www.weatherapi.com/","Category":"Weather"},
    {"API":"Open-Meteo","Description":"Free weather forecast API — no key needed","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://open-meteo.com/","Category":"Weather"},
    {"API":"Tomorrow.io","Description":"Hyperlocal weather intelligence and climate risk","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://www.tomorrow.io/","Category":"Weather"},
    {"API":"National Weather Service","Description":"NOAA forecasts and alerts for the US","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.weather.gov/","Category":"Weather"},
    {"API":"AerisWeather","Description":"Professional weather data and global imagery","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://www.aerisweather.com/","Category":"Weather"},
    {"API":"Alpha Vantage","Description":"Free stock prices, FX rates and indicators","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://www.alphavantage.co/","Category":"Finance"},
    {"API":"CoinGecko","Description":"Free crypto data — prices, market cap, history","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.coingecko.com/","Category":"Finance"},
    {"API":"Polygon.io","Description":"Real-time stocks, options, forex and crypto","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://polygon.io/","Category":"Finance"},
    {"API":"Exchange Rate API","Description":"Currency conversion and exchange rate data","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://www.exchangerate-api.com/","Category":"Finance"},
    {"API":"Open Exchange Rates","Description":"Currency rates and converter with history","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://openexchangerates.org/","Category":"Finance"},
    {"API":"CoinLore","Description":"Cryptocurrency price data for 5000+ coins","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.coinlore.com/","Category":"Finance"},
    {"API":"CoinCap","Description":"Real-time cryptocurrency rates and history","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://coincap.io/","Category":"Finance"},
    {"API":"Binance","Description":"Crypto exchange prices and order book data","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://binance-docs.github.io/","Category":"Finance"},
    {"API":"Financial Modeling Prep","Description":"Financial statements, ratios and stock data","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://site.financialmodelingprep.com/","Category":"Finance"},
    {"API":"Google Maps","Description":"Geocoding, directions, places and maps","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://developers.google.com/maps","Category":"Maps"},
    {"API":"Mapbox","Description":"Custom maps, geocoding and navigation","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://www.mapbox.com/","Category":"Maps"},
    {"API":"OpenStreetMap Nominatim","Description":"Free geocoding using OSM data — no key","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://nominatim.org/","Category":"Maps"},
    {"API":"IPGeolocation","Description":"IP to location with timezone and currency","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://ipgeolocation.io/","Category":"Maps"},
    {"API":"Rest Countries","Description":"Country names, capitals, currencies and flags","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://restcountries.com/","Category":"Maps"},
    {"API":"IP-API","Description":"IP address to country, region, city and ISP","Auth":"","HTTPS":False,"Cors":"yes","Link":"http://ip-api.com/","Category":"Maps"},
    {"API":"OpenTopoData","Description":"Global elevation API using terrain datasets","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.opentopodata.org/","Category":"Maps"},
    {"API":"NewsAPI","Description":"Search articles from 75,000+ sources worldwide","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://newsapi.org/","Category":"News"},
    {"API":"The Guardian","Description":"Content API for Guardian articles and sections","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://open-platform.theguardian.com/","Category":"News"},
    {"API":"New York Times","Description":"Article search, top stories and movie reviews","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://developer.nytimes.com/","Category":"News"},
    {"API":"Dev.to","Description":"Developer community articles, tags and comments","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://developers.forem.com/","Category":"News"},
    {"API":"Hacker News","Description":"Official HN stories, comments, jobs and polls","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://github.com/HackerNews/API","Category":"News"},
    {"API":"GitHub","Description":"Repos, commits, issues, gists and developer data","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://docs.github.com/en/rest","Category":"Social"},
    {"API":"Reddit","Description":"Subreddits, posts, comments and user data","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://www.reddit.com/dev/api/","Category":"Social"},
    {"API":"Telegram Bot","Description":"Create bots with messaging and keyboards","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://core.telegram.org/bots/api","Category":"Social"},
    {"API":"Discord","Description":"Build bots, manage servers and messages","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://discord.com/developers/docs","Category":"Social"},
    {"API":"Mastodon","Description":"Decentralized open-source social network API","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://docs.joinmastodon.org/api/","Category":"Social"},
    {"API":"TMDB","Description":"Movies, TV shows, actors and trailers database","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://developer.themoviedb.org/","Category":"Entertainment"},
    {"API":"OMDB","Description":"Open Movie Database for detailed film info","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://www.omdbapi.com/","Category":"Entertainment"},
    {"API":"RAWG","Description":"Largest game database — 500,000+ games","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://rawg.io/apidocs","Category":"Entertainment"},
    {"API":"Jikan","Description":"Unofficial MyAnimeList REST API — anime data","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://jikan.moe/","Category":"Entertainment"},
    {"API":"JokeAPI","Description":"Programming, dark and misc jokes API","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://sv443.net/jokeapi/v2/","Category":"Entertainment"},
    {"API":"Open Trivia DB","Description":"Free trivia questions in multiple categories","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://opentdb.com/","Category":"Entertainment"},
    {"API":"Cocktail DB","Description":"Worldwide cocktail and drink recipes","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.thecocktaildb.com/","Category":"Entertainment"},
    {"API":"Meal DB","Description":"Worldwide meals with ingredients and instructions","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.themealdb.com/","Category":"Entertainment"},
    {"API":"Giphy","Description":"Search and discover millions of GIFs","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://developers.giphy.com/","Category":"Entertainment"},
    {"API":"Chuck Norris Facts","Description":"Random Chuck Norris jokes with categories","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://api.chucknorris.io/","Category":"Entertainment"},
    {"API":"Spotify","Description":"Music catalog, playlists and audio features","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://developer.spotify.com/","Category":"Music"},
    {"API":"Last.fm","Description":"Music scrobbling, charts and artist info","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://www.last.fm/api","Category":"Music"},
    {"API":"Deezer","Description":"Music streaming with artists and playlists","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://developers.deezer.com/","Category":"Music"},
    {"API":"MusicBrainz","Description":"Open music encyclopedia with recordings","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://musicbrainz.org/doc/MusicBrainz_API","Category":"Music"},
    {"API":"Genius","Description":"Song lyrics annotations and artist information","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://docs.genius.com/","Category":"Music"},
    {"API":"NASA","Description":"Astronomy images, space data and Mars rover photos","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://api.nasa.gov/","Category":"Science"},
    {"API":"SpaceX API","Description":"Rockets, launches, capsules and launchpad data","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://github.com/r-spacex/SpaceX-API","Category":"Science"},
    {"API":"Open Notify","Description":"ISS location and astronauts in space count","Auth":"","HTTPS":True,"Cors":"no","Link":"http://open-notify.org/","Category":"Science"},
    {"API":"arXiv","Description":"Preprints in physics, math, CS and biology","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://info.arxiv.org/help/api/","Category":"Science"},
    {"API":"Wikipedia","Description":"Articles, summaries and search data","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.mediawiki.org/wiki/API","Category":"Science"},
    {"API":"Free Dictionary","Description":"Open-source English dictionary with phonetics","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://dictionaryapi.dev/","Category":"Science"},
    {"API":"Google Books","Description":"Search millions of books and previews","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://developers.google.com/books/","Category":"Science"},
    {"API":"Open Library","Description":"Millions of free e-books with metadata","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://openlibrary.org/developers","Category":"Science"},
    {"API":"Datamuse","Description":"Word-finding engine — rhymes, synonyms, related","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.datamuse.com/api/","Category":"Science"},
    {"API":"JSONPlaceholder","Description":"Free fake REST API for testing — no auth needed","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://jsonplaceholder.typicode.com/","Category":"Utilities"},
    {"API":"Httpbin","Description":"HTTP request and response testing service","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://httpbin.org/","Category":"Utilities"},
    {"API":"IPify","Description":"Simple scalable public IP address API","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.ipify.org/","Category":"Utilities"},
    {"API":"QR Code Generator","Description":"Generate QR codes for URLs and text content","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://goqr.me/api/","Category":"Utilities"},
    {"API":"Sunrise Sunset","Description":"Accurate sunrise and sunset times worldwide","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://sunrise-sunset.org/api","Category":"Utilities"},
    {"API":"Random.org","Description":"True random numbers from atmospheric noise","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://www.random.org/","Category":"Utilities"},
    {"API":"Bitly","Description":"URL shortening and link management platform","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://dev.bitly.com/","Category":"Utilities"},
    {"API":"DuckDuckGo Instant","Description":"Instant answers and definitions, no tracking","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://duckduckgo.com/","Category":"Utilities"},
    {"API":"GitHub Gist","Description":"Create and manage public and secret code snippets","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://docs.github.com/en/rest/gists","Category":"Development"},
    {"API":"Stack Overflow","Description":"Q&A data, profiles and developer insights","Auth":"OAuth","HTTPS":True,"Cors":"yes","Link":"https://api.stackexchange.com/","Category":"Development"},
    {"API":"PyPI","Description":"Python Package Index metadata API","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://warehouse.pypa.io/","Category":"Development"},
    {"API":"npm Registry","Description":"npm package metadata and download counts","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.npmjs.com/","Category":"Development"},
    {"API":"Bundlephobia","Description":"Find cost of adding an npm package to bundle","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://bundlephobia.com/","Category":"Development"},
    {"API":"Advice Slip","Description":"Random advice slips for your applications","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://api.adviceslip.com/","Category":"Fun"},
    {"API":"Bored API","Description":"Suggest activities when you are bored","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://www.boredapi.com/","Category":"Fun"},
    {"API":"Numbers API","Description":"Facts about numbers, dates and math","Auth":"","HTTPS":False,"Cors":"no","Link":"http://numbersapi.com/","Category":"Fun"},
    {"API":"Agify","Description":"Predict likely age from a first name","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://agify.io/","Category":"Fun"},
    {"API":"Yes/No","Description":"Random yes or no answer with a GIF","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://yesno.wtf/api","Category":"Fun"},
    {"API":"Kanye Quotes","Description":"Random Kanye West quotes REST API","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://kanye.rest/","Category":"Fun"},
    {"API":"OpenFDA","Description":"FDA drug, device and food safety data","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://open.fda.gov/apis/","Category":"Health"},
    {"API":"Disease.sh","Description":"Open disease data and COVID-19 statistics","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://disease.sh/","Category":"Health"},
    {"API":"Nutritionix","Description":"World largest verified nutrition database","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://developer.nutritionix.com/","Category":"Health"},
    {"API":"OpenAQ","Description":"Real-time and historical air quality worldwide","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://docs.openaq.org/","Category":"Environment"},
    {"API":"USGS Earthquake","Description":"Real-time earthquake data and seismic hazards","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://earthquake.usgs.gov/","Category":"Environment"},
    {"API":"Data.gov","Description":"US government open data — 300,000+ datasets","Auth":"apiKey","HTTPS":True,"Cors":"yes","Link":"https://data.gov/","Category":"Government"},
    {"API":"World Bank","Description":"Global development indicators and statistics","Auth":"","HTTPS":True,"Cors":"yes","Link":"https://datahelpdesk.worldbank.org/","Category":"Government"},
]

API_SOURCE = "https://api.publicapis.org/entries"


# ── Helper: fetch live or fallback ────────────────────────────────
def get_all_apis():
    try:
        response = requests.get(API_SOURCE, timeout=5)
        data = response.json()
        live = data.get("entries", [])
        if live:
            return live[:500]
    except Exception:
        pass
    return EMBEDDED_APIS


# ── Helper: code templates per language ───────────────────────────
CODE_TEMPLATES = {
    "Python": (
        'import requests\n\n'
        'url = "{endpoint}"\n\n'
        'response = requests.get(url)\n'
        'data = response.json()\n\n'
        'print(data)\n'
    ),
    "JavaScript": (
        'fetch("{endpoint}")\n'
        '  .then(response => response.json())\n'
        '  .then(data => {{\n'
        '    console.log(data);\n'
        '  }})\n'
        '  .catch(error => console.error("Error:", error));\n'
    ),
    "Node.js": (
        'const axios = require("axios");\n\n'
        'const url = "{endpoint}";\n\n'
        'axios.get(url)\n'
        '  .then(response => {{\n'
        '    console.log(response.data);\n'
        '  }})\n'
        '  .catch(error => {{\n'
        '    console.error("Error:", error.message);\n'
        '  }});\n'
    ),
    "Java": (
        'import java.net.http.HttpClient;\n'
        'import java.net.http.HttpRequest;\n'
        'import java.net.http.HttpResponse;\n'
        'import java.net.URI;\n\n'
        'HttpClient client = HttpClient.newHttpClient();\n\n'
        'HttpRequest request = HttpRequest.newBuilder()\n'
        '    .uri(URI.create("{endpoint}"))\n'
        '    .GET()\n'
        '    .build();\n\n'
        'HttpResponse<String> response = client.send(\n'
        '    request, HttpResponse.BodyHandlers.ofString()\n'
        ');\n\n'
        'System.out.println(response.body());\n'
    ),
}


# ═══════════════════════════════════════════════════════════════════
#  ROUTES
# ═══════════════════════════════════════════════════════════════════

# ── / — Home page ─────────────────────────────────────────────────
@app.route("/")
def home():
    apis         = get_all_apis()
    categories   = sorted(set(a.get("Category", "") for a in apis if a.get("Category")))
    selected_cat = request.args.get("cat", "")
    if selected_cat:
        apis = [a for a in apis if a.get("Category") == selected_cat]
    total = len(get_all_apis())
    return render_template("index.html", apis=apis, categories=categories,
                           selected_cat=selected_cat, total=total)


# ── /signup — Create account ──────────────────────────────────────
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("All fields are required.", "error")
            return render_template("signup.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("signup.html")

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "error")
            return render_template("signup.html")

        if User.query.filter_by(username=username).first():
            flash("That username is already taken.", "error")
            return render_template("signup.html")

        user = User(username=username, email=email,
                    password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        session["user_id"]  = user.id
        session["username"] = user.username
        flash("Account created! Welcome to DevAPI Hub.", "success")
        return redirect(url_for("home"))

    return render_template("signup.html")


# ── /login — Sign in ──────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user     = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Incorrect email or password.", "error")
            return render_template("login.html")

        session["user_id"]  = user.id
        session["username"] = user.username
        flash(f"Welcome back, {user.username}!", "success")
        return redirect(url_for("home"))

    return render_template("login.html")


# ── /logout — Sign out ────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


# ── /profile — User dashboard ─────────────────────────────────────
@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please log in to view your profile.", "error")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("login"))

    return render_template("profile.html", user=user, apis=user.apis)


# ── /admin — Add new API ──────────────────────────────────────────
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "user_id" not in session:
        flash("Please log in to add an API.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        name        = request.form.get("name", "").strip()
        tech        = request.form.get("tech", "").strip()
        url         = request.form.get("url", "").strip()
        description = request.form.get("desc", "").strip()
        code        = request.form.get("code", "").strip()
        endpoint    = request.form.get("endpoint", "").strip()

        if not all([name, tech, url, description, endpoint]):
            flash("Name, category, URL, description and endpoint are all required.", "error")
            return render_template("admin.html")

        if not code:
            code = f'import requests\nres = requests.get("{endpoint}")\nprint(res.json())'

        new_api = API(name=name, tech=tech, url=url, description=description,
                      code=code, endpoint=endpoint, method="GET",
                      user_id=session["user_id"])
        db.session.add(new_api)
        db.session.commit()
        flash(f'✅ API "{name}" added to the directory!', "success")
        return redirect(url_for("home"))

    return render_template("admin.html")


# ── /delete/<id> — Remove an API ──────────────────────────────────
@app.route("/delete/<int:api_id>")
def delete_api(api_id):
    if "user_id" not in session:
        flash("Please log in first.", "error")
        return redirect(url_for("login"))

    api = API.query.get_or_404(api_id)

    if api.user_id != session["user_id"]:
        flash("You can only delete your own APIs.", "error")
        return redirect(url_for("profile"))

    db.session.delete(api)
    db.session.commit()
    flash("API removed.", "info")
    return redirect(url_for("profile"))


# ── /generate/<id> — Code generator ──────────────────────────────
@app.route("/generate/<int:api_id>", methods=["GET", "POST"])
def generate(api_id):
    api = API.query.get_or_404(api_id)

    if request.method == "POST":
        language = request.form.get("language", "Python")
        template = CODE_TEMPLATES.get(language, CODE_TEMPLATES["Python"])
        code     = template.format(endpoint=api.endpoint)
        return render_template("result.html", code=code, language=language, api=api)

    return render_template("generate.html", api=api)


# ── Init DB tables and start server ──────────────────────────────
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
