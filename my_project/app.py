from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)

# Setup Flask-Babel for language support
app.config['BABEL_DEFAULT_LOCALE'] = 'en'  # Set default language to English
babel = Babel(app)

# Language selection logic
@babel.localeselector
def get_locale():
    # Choose the locale based on the user’s browser settings or URL parameter
    return request.accept_languages.best_match(['en', 'es', 'fr', 'zh'])

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
