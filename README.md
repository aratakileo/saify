# Saify

Interprete programming language, working by `Python`. Syntax similar to `SQL` + `Assembler`

### Run code (Example)
All files with code written in this language have the extension `.sai`.

Code in `main.py`
```py
from compiler import Compiler


compiler = Compiler(
   True,       # True - is file path, False - is code witten on Saify
   'main.sai'  # file with our code written on Saify

               # if you change first parameter to False then
               # you can insert code written on Saify instead file path
)
compiler.run()
```

Code in `main.sai`
```py
include "Lib/random.sai"

def print __Object
output __Object endl
enddef

print 'For help insert -> help'

set anchor1 __line__

input line 'Insert command -> '

set statement line

use statement
== 'help'

if statement goto 20
goto 27
output """Commands list:
help - commamds list
random - generate random number from 1 to 100
exit - close program
"""
goto anchor1

set statement line
== 'random'

if statement goto 33
goto 38

use line
randint 1 100
print line
goto anchor1

set statement line
== 'exit'

if statement goto 44
goto 46

exit 'Finishing -> Successful'

output 'Command \''
output line
output '\' is doesn\'t exists!' endl

goto anchor1
```
