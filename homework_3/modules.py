#!/usr/bin/python

import sys
import re

text = ''.join([line for line in sys.stdin])

modules = set()

module_string = r'[\.a-zA-Z]+'

first_match = re.findall(r'from +{} +import'.format(module_string), text)
for match in first_match:
    module = re.findall(module_string, match)[1]
    modules.add(module)

for match in first_match:
    text = text.replace(match, '')

second_match = re.finditer(
    r'import +({string})( *, *{string})*'.format(string=module_string),
    text
)

for match in second_match:
    parts = match.group(0).split(',')
    parts[0] = parts[0][6:].strip()
    for i in range(1, len(parts)):
        parts[i] = parts[i].strip()
    for part in parts:
        modules.add(part)

sorted_modules = [module for module in modules]
sorted_modules.sort()
print(', '.join(sorted_modules))
