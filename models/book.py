from src.db import db


class BookModel(db.Model):

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    genre = db.Column(db.String(255))

    library_id = db.Column(db.Integer, db.ForeignKey('libraries.id'))
    store = db.relationship('LibraryModel')

    def __init__(self, name, genre, library_id):
        self.name = name
        self.genre = genre
        self.library_id = library_id

    def json(self):
        return {'name': self.name, 'genre': self.genre, 'store_id': self.library_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_genre(cls, genre):
        return cls.query.filter_by(genre=genre).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
