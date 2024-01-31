from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)
books_server_url = "http://books-server.b9hshcbwdmhzeehy.uksouth.azurecontainer.io:5000"

app.static_folder = ''
app.template_folder = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books', methods=['GET'])
def get_books():

    response = requests.get(f'{books_server_url}/books')

    if response.status_code == 200:
        books = response.json()

        book_id = request.args.get('book_id')
        genre = request.args.get('genre')
        author = request.args.get('author')
        publication_year = request.args.get('publication_year')
        title = request.args.get('title')

        filtered_books = books

        if book_id:
            filtered_books = [book for book in filtered_books if book_id.lower() in str(book.get('id', '')).lower()]

        if genre:
            filtered_books = [book for book in filtered_books if genre.lower() in book.get('genre', '').lower()]

        if author:
            filtered_books = [book for book in filtered_books if author.lower() in book.get('author', '').lower()]

        if publication_year:
            filtered_books = [book for book in filtered_books if publication_year.lower() in str(book.get('publication_year', '')).lower()]

        if title:
            filtered_books = [book for book in filtered_books if title.lower() in book.get('title', '').lower()]

        if filtered_books:
            return jsonify(filtered_books)
        else:
            return jsonify({'message': 'No books found for the specified criteria.'}), 404
    else:
        return jsonify({'message': 'Failed to fetch data from the Books Server.'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

