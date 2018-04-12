from flask import Flask
from flask_restful import Api

from src.resources.book import Book, Books
from src.resources.library import Libraries, Library

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # You can change the sqlite to most other SQL DB. ex: MySQL,PostresSQL, etc.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "jack"
api = Api(app)


@app.before_first_request
def create_tables():
    from src.db import db
    db.init_app(app)
    db.create_all()


api.add_resource(Library, '/library/<string:name>')
api.add_resource(Libraries, '/libraries')

api.add_resource(Book, '/book/<string:name>')
api.add_resource(Books, '/books')

if __name__ == '__main__':
    app.run(debug=True)
