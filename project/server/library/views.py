from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
import json

from project.server import db, app
from project.server.models import User, Books

books_blueprint = Blueprint('books', __name__)

class GetBookListAPI(MethodView):
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                books = Books.query.order_by(Books.name).all()
                booklist = []
                if not books:
                    responseObject = {
                    'status': 'fail',
                    'message': 'Sorry. No books are available right now.'
                    }
                    return make_response(jsonify(responseObject)), 200
                for book in books:
                    booklist.append({
                        'id': book.id,
                        'name': book.name,
                        'author': book.author,
                        'isbn': book.isbn,
                        'summary': book.summary
                    })
                responseObject = {
                    'status': 'success',
                    'data': booklist
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


book_list_view = GetBookListAPI.as_view('book_list_api')

books_blueprint.add_url_rule(
    '/api/v1/books/getall',
    view_func=book_list_view,
    methods=['GET']
)