from flask import Flask, request, abort
import logging
import sys
sys.path.insert(0,"../../")
from src.config.config import ConfigParser
import requests

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Load GitHub token from environment variables
parser = ConfigParser('../config/config.ini')
token = parser.get_token()
if not token:
    logger.error("GITHUB_TOKEN not set in environment variables")
    sys.exit(1)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/webhook", methods=['POST'])
def handle_webhook():
    # Handle the webhook event
    data = request.get_json()
    logger.info("Received webhook event: %s", data.get('action'))
    if data is None:
        print("No JSON data in request")
        abort(400)
    print("Received webhook event: ", data.get('action'))
    if data.get('action') == 'opened':
        issue_comment(data)
    return "", 200


def issue_comment(data):
    # Use GitHub API to post a comment
    headers = {
        'Authorization': 'token ' + token,
        'Accept': 'application/vnd.github.v3+json',
    }
    comment = {
        'body': 'Hello, thank you for opening this issue! We will get back to you soon.'
    }
    url = f"https://api.github.com/repos/{data['repository']['owner']['login']}/{data['repository']['name']}/issues/{data['issue']['number']}/comments"
    logger.info("Posting comment to URL: %s", url)
    response = requests.post(url, headers=headers, json=comment)
    if response.status_code != 201:
        logger.error("Failed to post comment: %s", response.text)
    else:
        logger.info("Comment posted successfully")

if __name__ == "__main__":
    app.run(debug=True)
