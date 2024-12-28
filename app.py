from flask import Flask, jsonify, request, send_from_directory
from pymongo import MongoClient
from twitter_scrape import scrape_twitter
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__, static_folder="frontend/dist")

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI") 
client = MongoClient(MONGO_URI)
db = client["twitter_trends_db"]  # Database 
collection = db["trends"]  # Collection

# API route for scraping trends
@app.route("/scrape", methods=["POST"])
def scrape():
    cookies_file_path = "cookies/twitter_cookies.json"
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

# API route for fetching the most recent trends from MongoDB

@app.route("/recent-trends", methods=["GET"])
def recent_trends():
    # Fetch the most recent trends entry from the database
    recent_entry = collection.find_one(sort=[("_id", -1)])  # Sort by _id in descending order
    if recent_entry and "trends" in recent_entry:
        return jsonify({"trends": recent_entry["trends"]})
    else:
        # Return an empty list if no data is found
        return jsonify({"trends": [], "message": "No trends found in the database."})


# Route to serve React app in production
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
