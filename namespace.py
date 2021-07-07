from errors_manager import *


class Namespace:
    def __init__(self, namespace=..., error_manager: ErrorManager = ..., **kwargs):
        self.__namespace__ = namespace if isinstance(namespace, dict) else \
            namespace.__namespace__ if isinstance(namespace, Namespace) else {}

        self.__namespace__.update(kwargs)
        self.error_manager = error_manager if isinstance(error_manager, ErrorManager) else ErrorManager()

    def __repr__(self):
        res = ''

        keys = list(self.__namespace__.keys())

        for i in range(len(keys)):
            key = keys[i]
            res += f'\n{repr(key)}: {repr(self[key])}{"," if i != len(keys) - 1 else ""}'

        return f'{self.__class__.__name__}: {{{res}\n}}'

    def __getitem__(self, key):
        if key in self.__namespace__:
            return self.__namespace__[key]
        else:
            self.error_manager.append(
                Error(f'File "{self["__file__"]}", line {self["__line__"]}\nNameError: name \'{key}\' is not defined')
            )

    def __contains__(self, key):
        return key in self.__namespace__

    def __delitem__(self, key):
        del self.__namespace__[key]

    def __setitem__(self, key, value):
        self.__namespace__[key] = value

    def keys(self):
        return self.__namespace__.keys()

    def values(self):
        return self.__namespace__.values()

    def update(self, namespace=..., **kwargs):
        self.__namespace__.update(Namespace(namespace).__namespace__)
        self.__namespace__.update(kwargs)

    def clear(self):
        self.__namespace__ = {}
