from flask_restful import Resource
from src.models.library import LibraryModel

class Library(Resource):

    def get(self, name):
        store = LibraryModel.find_by_name(name)
        if store:
            return store.json()

        return {'message': "Library not found"}, 404

    def post(self, name):
        if LibraryModel.find_by_name(name):
            return {"message": f"A library with the name '{name}' already exists."}, 400

        library = LibraryModel(name)
        try:
            library.save_to_db()
        except:
            return {"message": "An error occurred while creating the store"}, 500

        return library.json(), 201

    def delete(self, name):
        library = LibraryModel.find_by_name(name)

        if library:
            library.delete_from_db()

        return {'message': 'Library deleted'}

class Libraries(Resource):
    def get(self):
        return {'libraries': [library.json() for library in LibraryModel.query.all()]}