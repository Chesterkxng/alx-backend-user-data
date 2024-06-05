#!/usr/bin/env python3
"""
class to manage the API authentication.
"""
from typing import List, TypeVar
from flask import request
import fnmatch


class Auth:
    """ class definition
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ check if auth is needed
        """
        if path is None or excluded_paths is None \
           or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ return the value of the header request Authorization
        """
        if request is not None:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return None for the moment
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
