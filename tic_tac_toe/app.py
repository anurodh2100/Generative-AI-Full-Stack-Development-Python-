from flask import Flask, send_from_directory, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

# Flask automatically serves static files from the 'static' folder.

if __name__ == '__main__':
    app.run(debug=True, port=5001)
