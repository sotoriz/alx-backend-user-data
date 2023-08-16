#!/usr/bin/env python3
""" A module to Query the web server """
import requests


def register_user(email: str, password: str) -> None:
    """ register a new user """
    x = requests.post('http://localhost:5000/users',
                      {'email': email, 'password': password})
    assert x.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """ login with a wrong password """
    x = requests.post('http://localhost:5000/sessions',
                      {'email': email, 'password': password})
    assert x.status_code == 401


def log_in(email: str, password: str) -> str:
    """ login with a correct password """
    x = requests.post('http://localhost:5000/sessions',
                      {'email': email, 'password': password})
    assert x.status_code == 200
    return x.cookies.get('session_id')


def profile_unlogged() -> None:
    """ profile unlogged"""
    x = requests.get('http://localhost:5000/profile')
    assert x.status_code == 403


def profile_logged(session_id: str) -> None:
    """ profile logged"""
    x = requests.get('http://localhost:5000/profile',
                     cookies={"session_id", session_id})
    assert x.status_code == 200


def log_out(session_id: str) -> None:
    """ log out"""
    x = requests.delete('http://localhost:5000/sessions',
                        cookies={"session_id", session_id})
    assert x.status_code == 200


def reset_password_token(email: str) -> str:
    """ reset password token """
    x = requests.post('http://localhost:5000/reset_password', {'email': email})
    assert x.status_code == 200


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ update password """
    x = requests.put('http://localhost:5000/reset_password', {'email': email,
                     'reset_token': reset_token, 'new_password': new_password})
    assert x.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
