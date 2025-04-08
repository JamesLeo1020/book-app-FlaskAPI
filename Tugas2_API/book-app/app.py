from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simpan data buku secara sederhana (tanpa database dulu)
books = []
book_id_counter = 1

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

@app.route('/api/books', methods=['POST'])
def add_book():
    global book_id_counter
    data = request.get_json()
    new_book = {
        "id": book_id_counter,
        "title": data["title"],
        "author": data["author"]
    }
    books.append(new_book)
    book_id_counter += 1
    return jsonify(new_book), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    for book in books:
        if book["id"] == book_id:
            book["title"] = data.get("title", book["title"])
            book["author"] = data.get("author", book["author"])
            return jsonify(book), 200
    return jsonify({"message": "Buku tidak ditemukan"}), 404

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book["id"] != book_id]
    return jsonify({"message": "Buku telah dihapus"}), 200

if __name__ == '__main__':
    app.run(debug=True)
