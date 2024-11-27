from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create a SQLite database
conn = sqlite3.connect('library.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY, title TEXT, author TEXT, genre TEXT, publication_date TEXT)''')
conn.commit()
conn.close()

# Define a function to search for books
def search_books(query):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?''', ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    results = c.fetchall()
    conn.close()
    return results

# Define a route for the search API
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = search_books(query)
    return jsonify(results)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)