
class NegativeNumberException(Exception):
    def __init__(self, todo_id) -> None:
        self.todo_id = todo_id