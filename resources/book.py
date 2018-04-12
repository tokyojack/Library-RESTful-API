from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from src.models.book import BookModel


class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('genre',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('library_id',
                        type=int,
                        required=True,
                        help="Every item needs a library id")

    def get(self, name):
        item = BookModel.find_by_name(name)

        if item:
            return item.json()

        return {'message': 'Book not found'}, 404

    def post(self, name):
        if BookModel.find_by_name(name):
            return {f"error": "An book with name '{name}' already exists"}, 400

        # TODO: self?
        data = Book.parser.parse_args()

        book = BookModel(name, **data)
        print(book.json())
        try:
            book.save_to_db()
        except Exception as asd:
            print(asd)
            return {"message": "An error occurred inserting the book"}, 500  # Internal Server error

        return book.json(), 201

    def delete(self, name):
        book = BookModel.find_by_name(name)
        if book:
            book.delete_from_db()
        return {'message': 'Book deleted'}

    def put(self, name):
        data = Book.parser.parse_args()
        book = BookModel.find_by_name(name)

        if book is None:
            book = BookModel(name, **data)
        else:
            book.price = data['price']

        book.save_to_db()

        return book.json()


class Books(Resource):

    def get(self):
        return {'books': [book.json() for book in BookModel.query.all()]}
