from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {'id': 1, 'title': '1984', 'author': 'George Orwell'},
    {'id': 2, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
    {'id': 3, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
    {'id': 4, 'title': 'Book 4', 'author': 'Author 4'},
    {'id': 5, 'title': 'Book 5', 'author': 'Author 5'},      
]

@app.route('/', methods=['GET'])
def home_page():
    return 'Home Page'

# route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# route to get a book by its ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404


# CREATE new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json

    # if not data or 'id' not in data or 'title' not in data or 'author' not in data:
    #     return jsonify({'error': 'Invalid input data'}), 400

    new_book = {
        'id': data['id'],
        'title': data['title'],
        'author': data['author']
    }

    books.append(new_book)
    return jsonify(new_book), 201



# UPDATE existing book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json

    for book in books:
        if book['id'] == book_id:
            book['title'] = data.get('title', book['title'])
            book['author'] = data.get('author', book['author'])
            return jsonify({'message': 'Book updated successfully'})

    return jsonify({'error': 'Book not found'}), 404

# DELETE book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return jsonify({'message': 'Book deleted successfully'})
    return jsonify({'error': 'Book not found'}), 404 


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

    