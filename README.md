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
- [`use`/`enduse`](#use-enduse)
   - [`use`/`enduse`](#use-enduse-1)
   - [Operators](#operators)
- [Functions](#functions)
   - [Initialize](#initialize-1)
   - [Call](#call)
   - [Keyword `return`](#keyword-return)
   - [Default functions](#default-functions)
- [Other](#other)
  - [If statement](#if-statement)
  - [Keyword `include`](#keyword-include)
  - [Keyword `goto`](#keyword-goto)
  - [Keyword `del`](#keyword-del)

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
Also multiline string
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

### `use`/`enduse`
#### `use`/`enduse`
This construction allows you to interact with the value of a variable (only one variable can be interacted with at a time).
Structure
```py
use <variable>
<code>
enduse
```
Example
```py
set val 1

use val
+ 1
* 2
** 2
- 4
/ 3
enduse

output val endl  # output: 4
```
#### Operators
| Operator | Description              |
|----------|--------------------------|
| `+`      | Add                      |
| `-`      | Minus                    |
| `**`     | Exponentiation           |
| `*`      | Multiplication           |
| `/`      | Division                 |
| `//`     | Integer division         |
| `%`      | Mod                      |
| `==`     | Equals                   |
| `!=`     | Not equals               |
| `<`      | Less than                |
| `>`      | Greater than             |
| `<=`     | Less than or equal to    |
| `>=`     | Greater than or equal to |
| `and`    | ...                      |
| `or`     | ...                      |
| `not`    | ...                      |
| `in`     | ...                      |
| `is`     | ...                      |

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

#### Keyword `return`
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

#### Default functions
`output` - print the specified values (structure `output <value>*` (any number of arguments))

`input` - enter a value from the keyboard (structure `input <variable-name> <value (to print)>?`)

`exit` - exiting the program with an indication of the reason (structure `exit <value (reason)>?`)

`eval` - execute the `Saify` code passed as a string value (structure `eval <value (Saify code)>`)

`pyeval` - execute the `Python` code passed as a string value (structure `eval <value (Python code)>`)

> [Navigation]

# Other
#### If statement
Structure
```py
if <value> <code>
```
Example
```py
set val 2
use val
+ 2
== 4

if val output "2 + 2 = 4" endl

2
+ 2
== 5

if val output "2 + 2 = 5" endl
```
or
```py
set name ''
input name 'What is your name? '

set statement False
use statement
!= ''
enduse

set IF __line__
use IF
+ 15
enduse

if statement goto IF

# ELSE
output "Hi!" endl

set ELSE __line__
use ELSE
+ 9
enduse
goto ELSE

# IF
output "Hi, " name " !" endl

# END
```

#### Keyword `include`
Allows you to connect modules written in `Saify` or `Python`.
Structure
```py
include <str>
```
Example
```py
include "Lib/math.sai"
```
#### Keyword `goto`
This keyword allows the program to proceed to code execution, starting from the specified line.
Structure
```py
goto <value>
```
Example
```py
goto 23
```

#### Keyword `del`
Allows you to delete variable.
Structure
```py
del <variable>
```
Example
```py
set val 12

del val

output val endl  # error
```
> [Navigation]
