from typing import NamedTuple
from errors_manager import *
from namespace import *
from tokentype import *
from dictaddon import *
from saitypes import *
from keywords import *
import os.path as _path
import straddon
import re

COMPILE_TYPE_DEFAULT = 0
COMPILE_TYPE_FUNCTION = 1
COMPILE_TYPE_MODULE = 2

global_import_namespace = globals()


def clear_namespace(namespace):
    for key in list(global_import_namespace.keys()):
        del namespace[key]


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


class Lexer:
    def __init__(self, ispath: bool, file: str, compile_type: int = COMPILE_TYPE_DEFAULT, line_offset: int = 1):
        self.path = ''
        self.file = file

        if ispath:
            self.path = file
            with open(file, 'r', encoding='utf-8') as f:
                self.file = f.read()

        self.error_manager = ErrorManager()
        self.compile_type = compile_type
        self.line_offset = line_offset

    def run(self):
        token_manager = []
        token_line = []
        sediment = 0
        def_config = AttributeDict({
            'opened': 0,
            'last_def_index': [],
            'last_enddef_index': []
        })

        def_config.init_is_ending = False

        keywords = list(Keywords.__dict__.values())
        del keywords[0], keywords[-3:]

        words_op = ['and', 'or', 'not', 'in', 'is']

        token_specifications = [
            (TokenType.MULTI_LINE_STR, r'\'\'\'.*\'\'\'|\"\"\".*\"\"\"'),
            (TokenType.NEW_LINE, r'\n'),
            (TokenType.COMMENT, r'#.[^\n]*|#.[^\n]*$'),
            (TokenType.STR, r'\'.[^\n]*\'|\".[^\n]*\"'),
            (TokenType.ELLIPSIS, r'\.\.\.'),
            (TokenType.ID, r'[A-Za-z_]+\d+|[A-Za-z_]+'),
            (TokenType.OP, r'\*\*|//|==|!=|>=|<=|[*\-+/<>%]'),
            (TokenType.FLOAT, r'\d+\.\d+'),
            (TokenType.INT, r'\d+'),
            (TokenType.SKIP, r'\W'),
            (TokenType.MISMATCH, '.+')
        ]
        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specifications)
        line_num = self.line_offset
        line_start = 0

        for mo in re.finditer(token_regex, self.file, re.DOTALL):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind in [TokenType.STR, TokenType.MULTI_LINE_STR]:
                value = value[1:-1]
                if kind == TokenType.MULTI_LINE_STR:
                    value = value[2:-2]
                    off = value.count('\n')
                    sediment += off
                value = straddon.replace(value, {
                    r'\n': '\n',
                    r'\b': '\b',
                    r'\f': '\f',
                    r'\r': '\r',
                    r'\t': '\t',
                    r"\'": '\'',
                    r'\"': '\"',
                    r'\\': '\\'
                })
            elif kind == TokenType.COMMENT:
                value = value[1:]
            elif kind == TokenType.FLOAT:
                value = float(value)
            elif kind == TokenType.INT:
                value = int(value)
            elif kind == TokenType.ID:
                if value in keywords:
                    kind = value

                    if kind == Keywords.DEF:
                        def_config.opened = def_config.opened + 1
                        def_config.last_def_index = [len(token_manager), len(token_line)]
                    elif kind == Keywords.ENDDEF:
                        def_config.opened = def_config.opened - 1
                        def_config.last_enddef_index = [len(token_manager), len(token_line)]
                    elif kind == Keywords.RETURN and not (self.compile_type == COMPILE_TYPE_FUNCTION or def_config != 0):
                        self.error_manager.append(
                            Error(f'File "{self.path}", line {line_num}\nSyntaxError: \'{value!r}\' outside function')
                        )
                        return self.error_manager
                elif value in words_op:
                    kind = TokenType.OP
            elif kind == TokenType.NEW_LINE:
                line_num += 1
            elif kind == TokenType.SKIP:
                continue
            elif kind == TokenType.MISMATCH:
                self.error_manager.append(
                    Error(f'File "{self.path}", line {line_num}\nUnexpected \'{value!r}\'')
                )
                return self.error_manager

            if def_config.opened > 0\
                    and kind not in [Keywords.DEF, TokenType.NEW_LINE]\
                    and def_config.init_is_ending:
                continue

            if kind == TokenType.NEW_LINE:
                if not def_config.init_is_ending and def_config.opened > 0:
                    def_config.init_is_ending = True
                elif def_config.opened == 0:
                    def_config.init_is_ending = False

                token_manager.append(token_line)
                token_line = []
            else:
                token_line.append(Token(type=kind, value=value, line=line_num, column=column))
                while sediment > 0:
                    token_manager.append([])
                    sediment -= 1
                    line_num += 1

            # print(f'{line_num}: {kind} -> "{value}"')

        token_manager.append(token_line)

        if def_config.opened != 0:
            __u_token_ = token_manager[def_config.last_def_index[0]][def_config.last_def_index[1]]

            if def_config.opened < 0:
                __u_token_ = token_manager[def_config.last_enddef_index[0]][def_config.last_enddef_index[1]]

            self.error_manager.append(
                Error(f'File "{self.path}", line {__u_token_.line}\nSyntaxError: unmatched \'{__u_token_.value!r}\'')
            )

            return self.error_manager

        return token_manager


class Compiler:
    def __init__(self, ispath: bool, file: str, compile_type: int = COMPILE_TYPE_DEFAULT, line_offset: int = 1):
        self.lexer = Lexer(ispath, file, compile_type, line_offset)
        self.error_manager = self.lexer.error_manager

    def run(self, namespace=...):
        lexer_out = self.lexer.run()
        if isinstance(lexer_out, ErrorManager):
            return lexer_out

        print(lexer_out)
        # print(f'{self.lexer.compile_type}: {self.lexer.line_offset}')
        # print(len(lexer_out))

        using_var = None

        if namespace is ...:
            namespace = Namespace()

        namespace.error_manager = self.lexer.error_manager
        namespace.update({
            '...': ...,
            'True': True,
            'False': False,
            'None': None,
            'endl': '\n',
            '__line__': 0,
            '__file__': _path.abspath(self.lexer.path),
            '__name__':
                '__main__' if 0 <= self.lexer.compile_type <= 1
                else '.'.join(_path.split(self.lexer.path)[-1].split('.')[:-1])
        })

        last_def = None

        def __compile(token: Token, args: list):
            nonlocal using_var, namespace, last_def

            def set_using_var(script: str):
                nonlocal using_var, namespace, token
                if using_var is not None:
                    val = namespace[args[0].value]
                    __namespace = {
                        'using_var': namespace[using_var],
                        'val': val
                    }
                    exec(script.format(token.value), __namespace)
                    namespace[using_var] = __namespace['using_var']

            if token.type == Keywords.SET:
                namespace[args[0].value] = namespace[args[1].value]
            elif token.type == Keywords.USE:
                using_var = args[0].value
            elif token.type == Keywords.ENDUSE:
                using_var = None
            elif token.type == Keywords.OUTPUT:
                print(*[namespace[arg.value] for arg in args], end='', sep='')
            elif token.type == Keywords.INPUT:
                namespace[args[0].value] = input('' if len(args) < 2 else namespace[args[1].value])
            elif token.type == Keywords.DEL:
                del namespace[args[0].value]
            elif token.type == Keywords.GOTO:
                return int(namespace[args[0].value]) - 1
            elif token.type == Keywords.IF:
                return None if not namespace[args[0].value] else __compile(args[1], args[2:])
            elif token.type == TokenType.OP:
                if token.value == 'not':
                    set_using_var('using_var = {} val')
                else:
                    set_using_var('using_var = using_var {} val')
            elif token.type == Keywords.TYPE:
                set_using_var('using_var = {}(val).__name__')
            elif token.type in [Keywords.STR, Keywords.INT, Keywords.BOOL, Keywords.FLOAT]:
                set_using_var('using_var = {}(val)')
            elif token.type == Keywords.EVAL_PYTHON:
                exec(namespace[args[0].value], namespace.__namespace__)
                del namespace['__builtins__']
            elif token.type == Keywords.EVAL:
                __compile__ = Compiler(False, namespace[args[0].value])
                __compile__return__ = __compile__.run(namespace)
                if isinstance(__compile__return__, dict):
                    ____file____, ____name____ = namespace['__file__'], namespace['__name__']
                    namespace.update(__compile__return__)
                    namespace['__file__'], namespace['__name__'] = ____file____, ____name____
            elif token.type == Keywords.DEF:
                # print(f'args = {args}')
                last_def = Function(args[0].value, namespace['__line__'], [] if len(args) == 0 else args[1:])
            elif token.type == Keywords.ENDDEF:
                if isinstance(last_def, Function):
                    script = '\n'.join(self.lexer.file.split('\n')[last_def.line_start:namespace['__line__'] - 1])
                    last_def.compiler = Compiler(False, script, COMPILE_TYPE_FUNCTION, last_def.line_start)
                    namespace[last_def.id] = last_def
                last_def = None
            elif token.type == Keywords.RETURN:
                namespace['$return'] = namespace[args[0].value]
            elif token.type == TokenType.ID:
                __res = namespace[token.value]
                if isinstance(__res, Function):
                    __res = __res.run(*[namespace[arg.value] for arg in args])

                    if isinstance(__res, ErrorManager):
                        self.lexer.error_manager.__list__ = __res.__list__
                        return None

                    if using_var is not None:
                        namespace[using_var] = __res['$return']
            elif token.type == Keywords.INCLUDE:
                for file in args:
                    file = str(namespace[file.value])

                    if file.endswith('.py'):
                        __namespace__ = {}

                        __namespace__.update(global_import_namespace)

                        __namespace__.update({
                            '__name__': '.'.join(_path.split(file)[-1].split('.')[:-1]),
                            '__file__': _path.split(file)
                        })

                        with open(file, 'r', encoding='utf-8') as f:
                            file = f.read()

                        exec(file, __namespace__)

                        clear_namespace(__namespace__)

                        namespace.update(__namespace__)
                    elif file.endswith('.sai'):

                        compiler = Compiler(True, file, COMPILE_TYPE_MODULE)
                        compile_out = compiler.run()

                        # print(compile_out)

                        if isinstance(compile_out, ErrorManager):
                            self.lexer.error_manager.__list__ = compile_out.__list__
                            return None

                        del compile_out['__file__'], compile_out['__name__']

                        namespace.update(compile_out)
            elif token.type == Keywords.EXIT:
                exit(0 if len(args) < 1 else namespace[args[0].value])

        memory_index = 0

        for i in range(len(lexer_out)):
            line = lexer_out[i]
            for j in range(len(line)):
                if line[j].type in [TokenType.INT, TokenType.STR, TokenType.MULTI_LINE_STR, TokenType.FLOAT]:
                    memory_name = f'0x{memory_index}'
                    namespace[memory_name] = line[j].value
                    lexer_out[i][j] = Token(type=TokenType.ID, value=memory_name, line=line[j].line,
                                            column=line[j].column)
                    memory_index += 1

        # print(lexer_out)

        i = 0
        while i < len(lexer_out):
            # print(i + 1)
            namespace['__line__'] = i + 1
            line = lexer_out[i]
            # print(line)
            for j in range(len(line)):
                token = line[j]
                index_start = 1
                index_end = len(line)

                # print(f'index_end = {index_end}')
                # print(f'index_start = {index_start}')

                if line[-1].type == TokenType.COMMENT:
                    index_end -= 1

                returned = __compile(token, line[index_start:index_end])

                if len(self.lexer.error_manager) > 0:
                    return self.lexer.error_manager

                i = i if returned is None else returned - 1

                break

            i += 1

        # print(namespace)

        return namespace
