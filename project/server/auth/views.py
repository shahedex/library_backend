from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
import json

from project.server import bcrypt, db, app
from project.server.models import User, BlacklistToken

auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    def post(self):
        response_msg = []
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        first_name = request.json.get('first_name', None)
        last_name = request.json.get('last_name', None)
        is_admin = request.json.get('is_admin', None)

        if not email:
            response_msg.append('email must be non-empty')
        if not password:
            response_msg.append('password must be non-empty')
        if not first_name:
            response_msg.append('first_name must be non-empty')
        if not last_name:
            response_msg.append('last_name must be non-empty')
        if is_admin is None:
            response_msg.append('is_admin must be non-empty')
        
        if len(response_msg) > 0:
            responseObject = {
                'status': 'failed',
                'message': response_msg
            }
            return make_response(jsonify(responseObject)), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            try:
                user = User(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_admin=is_admin
                )

                db.session.add(user)
                db.session.commit()
                
                auth_token = user.encode_auth_token(user.id, int(is_admin))
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


class LoginAPI(MethodView):
    def post(self):
        response_msg = []
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not email:
            response_msg.append('email must be non-empty')
        if not password:
            response_msg.append('password must be non-empty')

        if len(response_msg) > 0:
            responseObject = {
                'status': 'failed',
                'message': response_msg
            }
            return make_response(jsonify(responseObject)), 400
            
        try:
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(
                user.password, password
            ):
                auth_token = user.encode_auth_token(user.id, user.is_admin)
                # app.logger.debug(auth_token)
                if auth_token:
                    # app.logger.debug(user.first_name + ' successfully logged in')
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode(),
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            app.logger.debug(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


class LogoutAPI(MethodView):
    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                db.session.add(user)
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    db.session.add(blacklist_token)
                    db.session.commit()
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
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
            return make_response(jsonify(responseObject)), 403

            
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')


auth_blueprint.add_url_rule(
    '/api/v1/auth/register',
    view_func=registration_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/api/v1/auth/login',
    view_func=login_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/api/v1/auth/logout',
    view_func=logout_view,
    methods=['POST']
)