from flask import Flask, jsonify, send_file
from twitter_scrape import scrape_twitter
import os

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('templates/index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    cookies_file_path = "cookies/twitter_cookies.json"
    twitter_url = "https://x.com/home?lang=en"
    
    trends = scrape_twitter(twitter_url, cookies_file_path)
    return jsonify({"trends": trends})

if __name__ == '__main__':
    app.run(debug=True)