from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)


@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])


@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    book = Book(
        title=data["title"],
        author=data["author"],
        genre=data["genre"],
        publication_date=data["publication_date"],
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.json
    book.title = data["title"]
    book.author = data["author"]
    book.genre = data["genre"]
    book.publication_date = data["publication_date"]
    db.session.commit()
    return jsonify(book.to_dict())


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})


if __name__ == "__main__":
    app.run(debug=True)