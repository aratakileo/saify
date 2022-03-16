# Saify

Interprete programming language, working by `Python`. Syntax similar to `SQL` + `Assembler`

> [Syntax](#syntax)

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

# Syntax
### Navigation
[navigation]: #navigation

- [Types](#types)
   - [Boolean](#boolean)
   - [String](#string)
   - [Number](#number)
   - [Ellipsis](#ellipsis)
   - [None](#none)
- [Initialize variable](#initialize-variable)
- [Setting variable's value](#setting-variables-value)
- [Initialize function](#initialize-function)

### Types
##### Boolean
```py
True
```
```py
False
```
##### String
```py
'Hello World!'
```
```py
"Hello World!"
```
```py
'''Hello World!'''
```
```py
"""Hello World!"""
```
##### Number
```py
123
```
```py
123.4
```
##### Ellipsis
```py
...
```
##### None
```py
None
```
> [Navigation]

### Initialize variable
Structure
```sql
set <name> <value>
```

Example
```sql
set variable 123
```
> [Navigation]

### Setting variable's value
```sql
set variable 456
```
or
```sql
use variable
456
enduse
```
> [Navigation]

### Initialize function
Structure
```py
def <name> (<argument>,)*
<code>
enddef
```

Example
```py
def print arg
output arg endl
enddef
```
or
```py
def show arg1 arg2
output arg1 arg2 endl
enddef
```
> [Navigation]
