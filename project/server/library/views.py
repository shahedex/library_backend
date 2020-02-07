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


class AddBookAPI(MethodView):
    def post(self):
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
                user = User.query.filter_by(id=resp).first()
                if user.is_admin == 1:
                    response_msg = []
                    name = request.json.get('name', None)
                    author = request.json.get('author', None)
                    isbn = request.json.get('isbn', None)
                    summary = request.json.get('summary', None)

                    if not name:
                        response_msg.append('name must be non-empty')
                    if not author:
                        response_msg.append('author must be non-empty')
                    if not isbn:
                        response_msg.append('isbn must be non-empty')
                    if not summary:
                        response_msg.append('summary must be non-empty')
                    
                    if len(response_msg) > 0:
                        responseObject = {
                            'status': 'failed',
                            'message': response_msg
                        }
                        return make_response(jsonify(responseObject)), 400
                    try:
                        book_obj = Books(name, author, isbn, summary)
                        db.session.add(book_obj)
                        db.session.commit()

                        responseObject = {
                        'status': 'success',
                        'message': book_obj.name + ' has been added to the booklist.'
                        }
                        return make_response(jsonify(responseObject)), 400

                    except Exception as e:
                        app.logger.debug(e)
                        responseObject = {
                        'status': 'fail',
                        'message': 'Sorry. The action has failed because of duplicate entry. Please try again.'
                        }
                        return make_response(jsonify(responseObject)), 400
                else:
                    responseObject = {
                    'status': 'fail',
                    'message': 'Sorry. You are not authorized to do this action.'
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

class DeleteBookAPI(MethodView):
    def post(self):
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
                user = User.query.filter_by(id=resp).first()
                if user.is_admin == 1:
                    response_msg = []
                    book_id = request.json.get('book_id', None)

                    if not book_id:
                        response_msg.append('book_id must be non-empty')
                    
                    if len(response_msg) > 0:
                        responseObject = {
                            'status': 'failed',
                            'message': response_msg
                        }
                        return make_response(jsonify(responseObject)), 400
                    try:
                        book_obj = Books.query.filter_by(id=book_id).first()
                        if not book_obj:
                            responseObject = {
                            'status': 'failed',
                            'message': 'book_id is not valid. Please try with a valid book_id.'
                            }
                            return make_response(jsonify(responseObject)), 400

                        db.session.delete(book_obj)
                        db.session.commit()

                        responseObject = {
                        'status': 'success',
                        'message': book_obj.name + ' has been deleted from the booklist.'
                        }
                        return make_response(jsonify(responseObject)), 400

                    except Exception as e:
                        app.logger.debug(e)
                        responseObject = {
                        'status': 'fail',
                        'message': 'Sorry. The action has been failed. Please try again.'
                        }
                        return make_response(jsonify(responseObject)), 400
                else:
                    responseObject = {
                    'status': 'fail',
                    'message': 'Sorry. You are not authorized to do this action.'
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

class UpdateBookInfoAPI(MethodView):
    def post(self):
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
                user = User.query.filter_by(id=resp).first()
                if user.is_admin == 1:
                    response_msg = []
                    book_id = request.json.get('book_id', None)
                    name = request.json.get('name', None)
                    author = request.json.get('author', None)
                    isbn = request.json.get('isbn', None)
                    summary = request.json.get('summary', None)

                    if not name:
                        response_msg.append('name must be non-empty')
                    if not author:
                        response_msg.append('author must be non-empty')
                    if not isbn:
                        response_msg.append('isbn must be non-empty')
                    if not summary:
                        response_msg.append('summary must be non-empty')
                    if not book_id:
                        response_msg.append('book_id must be non-empty')
                    
                    if len(response_msg) > 0:
                        responseObject = {
                            'status': 'failed',
                            'message': response_msg
                        }
                        return make_response(jsonify(responseObject)), 400
                    try:
                        book_obj = Books.query.filter_by(id=book_id).first()
                        if not book_obj:
                            responseObject = {
                            'status': 'failed',
                            'message': 'book_id is not valid. Please try with a valid book_id.'
                            }
                            return make_response(jsonify(responseObject)), 400

                        book_obj.name = name
                        book_obj.author = author
                        book_obj.isbn = isbn
                        book_obj.summary = summary
                        db.session.commit()

                        responseObject = {
                        'status': 'success',
                        'message': book_obj.name + ' info has been updated..'
                        }
                        return make_response(jsonify(responseObject)), 400

                    except Exception as e:
                        app.logger.debug(e)
                        responseObject = {
                        'status': 'fail',
                        'message': 'Sorry. The action has been failed. Please try again.'
                        }
                        return make_response(jsonify(responseObject)), 400
                else:
                    responseObject = {
                    'status': 'fail',
                    'message': 'Sorry. You are not authorized to do this action.'
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
add_book_view = AddBookAPI.as_view('add_book_api')
delete_book_view = DeleteBookAPI.as_view('delete_book_api')
update_book_view = UpdateBookInfoAPI.as_view('update_book_api')

books_blueprint.add_url_rule(
    '/api/v1/books/getall',
    view_func=book_list_view,
    methods=['GET']
)

books_blueprint.add_url_rule(
    '/api/v1/books/add',
    view_func=add_book_view,
    methods=['POST']
)

books_blueprint.add_url_rule(
    '/api/v1/books/delete',
    view_func=delete_book_view,
    methods=['POST']
)

books_blueprint.add_url_rule(
    '/api/v1/books/update',
    view_func=update_book_view,
    methods=['POST']
)