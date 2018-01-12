import re

my_string = '%! @arg sdescr; A brief description of the function.'

opt_string = '%! @descr The steak house serves nice steak.'
opt_string = ' @opt hideparen::Undefined:: Do not add parentheses after the function name.'

match = re.search('\s*@(\S+)'
                  '(\s+(\S+))?'
                  '(\s*;\s*((\S+\s+)*(\S+)))?'
                  '\s*;\s*(.*)$', my_string)

print(match.groups())


match = re.search('\s*@(\S+)' # Match token
                  '(\s+((\S+?)(::(.+)::)?)(\s|$))?' # Match argument
                  '\s*(.*)$', opt_string)

print(match.groups())

token = match.group(1)
arg = match.group(4)
default = match.group(6)
text = match.group(8)

print('Token:   ' + str(token))
print('Arg:     ' + str(arg))
print('Default: ' + str(default))
print('Text:    ' + str(text))
