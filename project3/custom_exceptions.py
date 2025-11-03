from fastapi import HTTPException, status

class NegativeNumberException(Exception):
    def __init__(self, todo_id) -> None:
        self.todo_id = todo_id


def get_user_exception():
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate the credentials",
                                          headers={"WWW-Authenticate":"Bearer"},)
    return credentials_exception

def token_exception():
    token_exception_response = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Incorrect username or password",
                                             headers={"WWW-Authenticate":"Bearer"},)
    return token_exception_response