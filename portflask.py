# ─── Flask keep-alive server for Render ───────────────────────────────────────
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return 'Bot is running!'

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    flask_app.run(host="0.0.0.0", port=port)

# Start Flask in background thread so Render detects open port
threading.Thread(target=run_flask, daemon=True).start()
# ──────────────────────────────────────────────────────────────────────────────


#and ye sabse uper me lagaana hai jo niche likh rha hu just import wali line

from flask import Flask