from flask import Flask, render_template, request, redirect, jsonify, url_for, send_from_directory, abort
import openai
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__)

# Primary logo on the site (full lockup, clean typography, tech + growth motif).
BRAND_LOGO_FILE = "logo_2.png"
_logo_dir = os.path.join(os.path.dirname(__file__), "logo")
_ALLOWED_LOGO_FILES = frozenset(
    f
    for f in (os.listdir(_logo_dir) if os.path.isdir(_logo_dir) else [])
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".svg"))
)


@app.route("/brand/<path:filename>")
def brand_asset(filename):
    """Serve files from the project /logo folder for use in templates."""
    if filename not in _ALLOWED_LOGO_FILES:
        abort(404)
    return send_from_directory(os.path.join(app.root_path, "logo"), filename)


@app.context_processor
def inject_brand_logo_url():
    return {"brand_logo_url": url_for("brand_asset", filename=BRAND_LOGO_FILE)}


# OPENAI_API_KEY: set in .env (local), or in the host's environment (Render/Railway/etc.).
# Netlify env vars do not apply to this Flask app unless you add Netlify Functions that call OpenAI separately.
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        print("New Lead:", data)
        return redirect('/thank-you')
    return render_template('contact.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            ai_message = response.choices[0].message['content']
            return jsonify({'response': ai_message})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)