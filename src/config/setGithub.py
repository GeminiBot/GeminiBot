from config.config import ConfigParser
import requests

class SetGithub:
    def __init__(self, file_path):
        parser = ConfigParser(file_path)
        self.owner = parser.get_value('GITHUB', 'OWNER')
        self.repo = parser.get_value('GITHUB', 'REPO')
        self.token = parser.get_value('GITHUB', 'TOKEN')
    def get_webhook_id(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/hooks"
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching webhooks: {response.text}")
            return None

        webhooks = response.json()
        # Assuming you want the first webhook
        if webhooks:
            return webhooks[0]['id']
        return None

    def get_ngrok_link(self):
        webhook_id = self.get_webhook_id()
        if webhook_id:
            try:
                response = requests.get("http://localhost:4040/api/tunnels")
                if response.status_code == 200:
                    tunnels = response.json()["tunnels"]
                    for tunnel in tunnels:
                        if tunnel["proto"] == "https":
                            public_url = tunnel["public_url"]
                            public_url += "/webhook"
                            return public_url
                else:
                    print(f"Error fetching ngrok url: {response.text}")
                    return None
            except requests.exceptions.ConnectionError:
                print("Connection refused. Is ngrok running?")
                return None
        else:
            print("No webhook found")
            return None
    def update_webhook(self, webhook_id, token, payload_url):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/hooks/{webhook_id}"
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        # Update payload URL and content type
        data = {
            "config": {
                "url": payload_url,
                "content_type": "json"  # New Content-Type for the webhook
            }
        }
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"Error updating webhook: {response.text}")
        else:
            print("Webhook updated successfully")
