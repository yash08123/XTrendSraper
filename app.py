from flask import Flask, jsonify, request, send_from_directory
from pymongo import MongoClient
from twitter_scrape import scrape_twitter
import os
import json
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__, static_folder="frontend/dist")

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["twitter_trends_db"]
collection = db["trends"]

# Save cookies route
@app.route("/save-cookies", methods=["POST"])
def save_cookies():
    try:
        # Get cookies from the request body
        netscape_cookies = request.data.decode("utf-8")
        cookies_json = []

        # Parse the Netscape format into JSON
        for line in netscape_cookies.splitlines():
            if not line.startswith("#") and line.strip():
                parts = line.split("\t")
                if len(parts) == 7:
                    cookie = {
                        "domain": parts[0],
                        "httpOnly": parts[1].upper() == "TRUE",
                        "path": parts[2],
                        "secure": parts[3].upper() == "TRUE",
                        "expiry": int(parts[4]),
                        "name": parts[5],
                        "value": parts[6],
                    }
                    cookies_json.append(cookie)

        # Save cookies to file
        with open("cookies/twitter_cookies.json", "w") as file:
            json.dump(cookies_json, file, indent=4)

        return jsonify({"message": "Cookies saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Scrape trends route
@app.route("/scrape", methods=["POST"])
def scrape():
    cookies_file_path = "cookies/twitter_cookies.json"

    # Check if cookies exist
    if not os.path.exists(cookies_file_path):
        return jsonify({"error": "Cookies not provided."}), 400

    twitter_url = "https://x.com/home?lang=en"

    # Scrape trends
    trends = scrape_twitter(twitter_url, cookies_file_path)

    # Show trends to the user first
    response = {"trends": trends}

    # Save trends to MongoDB
    if trends:
        trends_data = {"trends": trends, "source": "Twitter"}
        collection.insert_one(trends_data)

    return jsonify(response)

# Recent trends route
@app.route("/recent-trends", methods=["GET"])
def recent_trends():
    recent_entry = collection.find_one(sort=[("_id", -1)])
    if recent_entry and "trends" in recent_entry:
        return jsonify({"trends": recent_entry["trends"]})
    else:
        return jsonify({"trends": [], "message": "No trends found in the database."})

# Serve React app
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
