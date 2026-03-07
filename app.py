from flask import Flask, render_template
import requests

app = Flask(__name__)

API_SOURCE = "https://api.publicapis.org/entries"

@app.route("/")
def home():

    try:
        response = requests.get(API_SOURCE)
        data = response.json()
        apis = data["entries"][:500]   # limit 500 APIs
    except:
        apis = []

    return render_template("index.html", apis=apis)


if __name__ == "__main__":
    app.run(debug=True)
