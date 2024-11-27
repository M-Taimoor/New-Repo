from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    publication_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Book {self.title}>'

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    # Remove stop words and stem words
    query_words = [stemmer.stem(word) for word in re.findall(r'\w+', query.lower()) if word not in stop_words]

    # Search for books matching the query
    books = Book.query.filter(Book.title.like(f'%{query}%') | Book.author.like(f'%{query}%')).all()

    # Format the search results
    results = [{'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'publication_date': book.publication_date} for book in books]

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)