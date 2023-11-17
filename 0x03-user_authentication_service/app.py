#!/usr/bin/env python3
from flask import (
        Flask, jsonify, request, abort, make_response, redirect, url_for)
from auth import Auth
from typing import Dict


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def user() -> Dict[str, str]:
    """
    Registers a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"
            })
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> Dict[str, str]:
    """
    Creates a new session for the user and stores the session ID as
    a cookie
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)

        response = make_response(jsonify({
            "email": email,
            "message": "logged in"
            }))
        response.set_cookie("session_id", session_id)

        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> Dict[str, str]:
    """
    Logs out a user
    """
    session_id = request.cookie.get('session_id')
    if session_id is None:
        abort(403)
    user = Auth.get_user_from_id(session_id)
    if user:
        Auth.destroy_session(user.id)
        return redirect(url_for('/'))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> Dict[str, str]:
    """
    Retrieves a user's profile
    """
    session_id = request.cookie.get('session_id')
    user = Auth.get_user_from_id(session_id)
    if user:
        response = make_response(jsonify({
            "email": user.email
            }), 200)
        return response
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
