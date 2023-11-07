#!/usr/bin/env python3
""" Template for all authentication system """
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a path requires authorization
        """
        if (path is None or excluded_paths is None
                or (path not in excluded_paths
                    and (path + '/') not in excluded_paths)):
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """
        Determines the presence of an Authorization header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        """
        return None
