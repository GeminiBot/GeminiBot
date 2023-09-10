#!/usr/bin/env python3
from flask import Flask, request, abort
import logging
import sys
from config.config import ConfigParser
from config.setGithub import SetGithub
from server.events.events import Events
import requests

class Server:
    def __init__(self, file_path):
        self.parser = ConfigParser(file_path)
        self.token = self.parser.get_token()
        if not self.token:
            self.logger.error("GITHUB_TOKEN not set in environment variables")
            sys.exit(1)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()
        self.github = SetGithub(file_path)
        self.events = Events(self.github, self.token, self.logger)
        self.app = Flask(__name__)
        print(self.github.owner)
        @self.app.route("/")
        def hello():
            return "Hello World!"

        @self.app.route("/webhook", methods=['POST'])
        def _handle_webhook():
            print("Webhook route called")
            return self.handle_webhook()

    def handle_webhook(self):
        # Handle the webhook event
        data = request.get_json()
        self.logger.info("Received webhook event: %s", data.get('action'))
        if data is None:
            print("No JSON data in request")
            abort(400)
        print("Received webhook event: ", data.get('action'))
        #if data.get('action') == 'opened':
        #    issue_comment(data)
        if data.get('action') == 'pinned':
            self.events.issue_comment(data)
            #modify_file(data)
        return "", 200

    def start_server(self, port):
        self.app.run(port=port)
