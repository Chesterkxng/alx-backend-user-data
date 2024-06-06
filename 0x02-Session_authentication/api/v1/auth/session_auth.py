#!/usr/bin/env python3
"""
This module for SessionAuth class
"""
from api.v1.auth.auth import Auth
import uuid
from api.v1.views.users import User


class SessionAuth(Auth):
    """
    SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ session creater
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ retrieve the user id base on ssid
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ retrieve user using ssid """

        session_id = self.session_cookie(request=request)
        user_id = self.user_id_for_session_id(session_id=session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes a user session
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
