from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create a SQLite database
conn = sqlite3.connect('library.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY, title TEXT, author TEXT, genre TEXT)''')
conn.commit()
conn.close()

# Search API endpoint
@app.route('/search', methods=['POST'])
def search():
    # Get search query from request body
    query = request.json.get('query', '')

    # Connect to the database
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Search for books matching the query
    c.execute('''SELECT id, title, author, genre FROM books
                 WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?''',
                 ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    results = c.fetchall()

    # Close the database connection
    conn.close()

    # Return the search results as JSON
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)