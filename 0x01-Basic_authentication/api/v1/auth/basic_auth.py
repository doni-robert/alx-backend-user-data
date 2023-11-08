#!/usr/bin/env python3
""" The BasicAuth module """
from api.v1.auth.auth import Auth
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ The BasicAuth class
    """
    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """
        Returns the Base64 part of the Authorization header for a
        Basic Authentication
        """
        if (authorization_header is None
                or type(authorization_header) is not str
                or authorization_header.startswith('Basic ') is False):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Returns the decoded value of a Base64 string
        """
        if (base64_authorization_header is None
                or type(base64_authorization_header) is not str):
            return None
        try:
            if base64.b64decode(base64_authorization_header):
                return (base64.b64decode(base64_authorization_header)
                        ).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value
        """
        if (decoded_base64_authorization_header is None
                or type(decoded_base64_authorization_header) is not str
                or ':' not in decoded_base64_authorization_header):
            return None, None
        details = decoded_base64_authorization_header.split(':')
        return details[0], details[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        """
        pass
