#!/usr/bin/env python3
"""
class to manage the API authentication.
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ class definition
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ check if auth is needed
        """
        if path is None or excluded_paths is None \
           or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        if path in excluded_paths:
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
