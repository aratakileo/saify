from compiler import Compiler


compiler = Compiler(
   True,       # True - is file path, False - is code witten on Saify
   'main.sai'  # file with our code written on Saify

               # if you change first parameter to False then
               # you can insert code written on Saify instead file path
)
compiler.run()
