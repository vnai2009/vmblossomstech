from flask import Flask
import serverless_wsgi

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from Flask on Netlify!"

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)