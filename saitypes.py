from namespace import *


class Function:
    def __init__(self, id: str, line_start: int, __args: list):
        self.id = id
        self.line_start = line_start
        self.args = [arg.value for arg in __args]
        self.compiler = None

    def run(self, *args):
        __namespace = Namespace({
            '$return': None
        })

        for i in range(len(self.args)):
            __namespace[self.args[i]] = None if i > len(args) - 1 else args[i]

        return self.compiler.run(__namespace)

    @property
    def code(self):
        return self.compiler.lexer.file

    def __repr__(self):
        return f'Function: {{{repr("args")}: {self.args}, {repr("code")}: {repr(self.code)}}}'
