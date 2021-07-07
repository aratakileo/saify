if __name__ == '__main__':
    from compiler import *
    l = Compiler(True, 'main.sai')
    print(l.run())
    # l.run()

    # import os.path
    #
    # file = 'Lib/test.py'
    #
    # with open(file, 'r', encoding='utf-8') as f:
    #     _file = f.read()
    #
    # exec(compile(_file, file, 'exec'))
