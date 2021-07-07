class Error:
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class ErrorManager:
    def __init__(self):
        self.__list__ = []

    def __repr__(self):
        out = ''
        for error in self.__list__:
            out += str(error) + '\n'

        return out

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.__list__)

    def append(self, error: Error):
        self.__list__.append(error)
