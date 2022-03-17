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
- [Variables](#variables)
   - [Initialize](#initialize)
   - [Setting value](#setting-value)
   - [Default variables](#default-variables)
- [Functions](#functions)
   - [Initialize](#initialize-1)
   - [Call](#call)
   - [Return value](#return-value)

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

### Variables
#### Initialize
Structure
```sql
set <name> <value>
```

Example
```sql
set variable 123
```

#### Setting value
```sql
set variable 456
```
or
```sql
use variable
456
enduse
```

#### Default variables
`__line__` - get current line number

`__file__` - get file path

`__name__` - get compilation file name

`endl` - `'\n'`

> [Navigation]

### Functions
#### Initialize
Structure
```py
def <name> <argument>*
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
output arg1 " " arg2 endl
enddef
```

#### Call
Structure
```py
<name> <argument>*
```
Example
```py
print "Hello World!"
```
or
```py
show "Hello" "World!"  # Output: Hello World!
```

#### Return value
Structure
```py
return <value>
```
Example
```py
def add left right

use left
+ right
enduse

return left
enddef

set num 0

use num
add 1 1
enduse

output num endl  # Output: 2
```

> [Navigation]
