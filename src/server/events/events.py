import base64
import requests

class Events:
    def __init__(self, github, token, logger):
        self.github = github
        self.token = token
        self.logger = logger
    def modify_file(self, data):
        headers = {
            'Authorization': 'token ' + self.token,
            'Accept': 'application/vnd.github.v3+json',
        }
        path = f"{data['issue']['number']}.txt"
        url = f"https://api.github.com/repos/{data['repository']['owner']['login']}/{data['repository']['name']}/contents/{path}"

        content = "The content of the file"  # Change this to the actual content
        encoded_content = base64.b64encode(content.encode()).decode()

        payload = {
            'message': 'Creating or updating a file',
            'content': encoded_content,
        }

        response = requests.put(url, headers=headers, json=payload)

        if response.status_code != 201:
            self.logger.error("Failed to create or update file: %s", response.text)
        else:
            self.logger.info("File created or updated successfully")
    def issue_comment(self, data):
        # Use GitHub API to post a comment
        headers = {
            'Authorization': 'token ' + self.token,
            'Accept': 'application/vnd.github.v3+json',
        }
        comment = {
            'body': 'Hello, thank you for opening this issue! We will get back to you soon.'
        }
        url = f"https://api.github.com/repos/{data['repository']['owner']['login']}/{data['repository']['name']}/issues/{data['issue']['number']}/comments"
        self.logger.info("Posting comment to URL: %s", url)
        response = requests.post(url, headers=headers, json=comment)
        if response.status_code != 201:
            self.logger.error("Failed to post comment: %s", response.text)
        else:
            self.logger.info("Comment posted successfully")
