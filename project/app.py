# from flask import Flask, render_template, request, session, redirect, url_for
# from flask_babel import Babel, _, format_currency, format_date
# from datetime import datetime

# app = Flask(__name__)
# app.config['BABEL_DEFAULT_LOCALE'] = 'en'
# app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'
# app.config['SECRET_KEY'] = 'your_secret_key'

# # Initialize Babel
# babel = Babel(app)
# app.jinja_env.globals['get_locale'] = lambda: session.get('lang', app.config['BABEL_DEFAULT_LOCALE'])

# # List of supported languages
# LANGUAGES = ['en', 'es']

# # Locale selector function for Babel
# def get_locale():
#     # Check if a language is set in the session
#     if 'lang' in session:
#         return session['lang']
    
#     # If no session language, detect based on browser settings
#     return request.accept_languages.best_match(LANGUAGES)

# # Initialize Babel with the locale selector function
# babel.init_app(app, locale_selector=get_locale)

# @app.route('/set_language/<lang>')
# def set_language(lang):
#     if lang in LANGUAGES:
#         session['lang'] = lang  # Set the selected language in the session
#     return redirect(url_for('index'))

# @app.route('/')
# def index():
#     # Sample data for rendering
#     product_name = _("Product Name")
#     price = 99.99
#     today = datetime.now()
    
#     return render_template(
#         'index.html',
#         product_name=product_name,
#         price=price,
#         today=today,
#         get_locale=get_locale  # Pass get_locale to the template
#     )

# # Currency and date formatting helpers
# def format_currency_helper(value, currency='USD'):
#     return format_currency(value, currency)

# def format_date_helper(value):
#     return format_date(value)

# # Expose helpers to templates
# app.jinja_env.globals['format_currency'] = format_currency_helper
# app.jinja_env.globals['format_date'] = format_date_helper

# if __name__ == '__main__':
#     app.run(debug=True)
