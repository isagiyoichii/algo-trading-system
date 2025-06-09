import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
from datetime import datetime
from dotenv import load_dotenv, set_key

# Load .env from root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
LOG_PATH = os.path.join(ROOT_DIR, "access_tokens.log")
load_dotenv(ENV_PATH)

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000"

kite = KiteConnect(api_key=API_KEY)

class TokenHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        request_token = params.get("request_token", [None])[0]

        if not request_token:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing request_token.")
            return

        try:
            data = kite.generate_session(request_token, api_secret=API_SECRET)
            access_token = data["access_token"]

            # Check if already logged
            already_logged = False
            if os.path.exists(LOG_PATH):
                with open(LOG_PATH, "r") as log_file:
                    already_logged = access_token in log_file.read()

            if not already_logged:
                with open(LOG_PATH, "a") as log_file:
                    log_file.write(f"{datetime.now()} - {access_token}\n")
                    print("📝 Logged new access token.")
            else:
                print("ℹ️ Access token already logged.")

            # Update .env file
            set_key(ENV_PATH, "ACCESS_TOKEN", access_token)
            print(f"✅ Access token saved to .env: {access_token}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h2>Access token captured, logged, and saved to .env successfully!</h2>")

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            error_msg = f"Error: {str(e)}"
            self.wfile.write(error_msg.encode("utf-8"))
            print(f"❌ Error while generating session: {error_msg}")

def run():
    login_url = kite.login_url()
    print(f"\n🔗 Click this link to login to Zerodha:\n{login_url}")
    print("🌐 Waiting for redirect on http://127.0.0.1:8000 ...\n")

    server = HTTPServer(("127.0.0.1", 8000), TokenHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()
