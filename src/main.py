from src.server.server import Server
import os
import time
import subprocess
import threading

def start_ngrok():
    print("Starting Ngrok Server !")
    ngrok_command = "ngrok http 5000"

    with open("ngrok_log.txt", "wb") as log_file:
        try:
            ngrok_process = subprocess.Popen(ngrok_command.split(), stdout=log_file, stderr=log_file)
        except FileNotFoundError:
            print("ngrok not found. Is it installed?")
            return
        except OSError:
            print("Error executing ngrok.")
            return
        except KeyboardInterrupt:
            print("Killing ngrok process")
            ngrok_process.kill()
            return

    print("ngrok process created with PID: %d" % ngrok_process.pid)
    print("ngrok log file: %s" % os.path.abspath(log_file.name))

def start_server():
    print("Starting Python Server !")
    app.start_server(5000)

app = Server('src/config/config.ini')

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    # Wait a bit for the server to initialize
    time.sleep(2)
    ngrok_thread = threading.Thread(target=start_ngrok)
    ngrok_thread.start()
    # Wait a bit for the server to initialize
    time.sleep(2)
    print("ngrok public url: %s" % app.github.get_ngrok_link())
    app.github.update_webhook(app.github.get_webhook_id(), app.token, app.github.get_ngrok_link())

