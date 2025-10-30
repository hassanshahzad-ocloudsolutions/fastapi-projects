
class NegativeNumberException(Exception):

    def __init__(self, books_to_return) -> None:
        self.books_to_return = books_to_return