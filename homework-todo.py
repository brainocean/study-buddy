from pprint import pprint
import sys
import os
import re
import docx2txt

# extract text
text = docx2txt.process(sys.argv[1])
text = text + '\n'

def group(seq, regex):
    g = []
    for el in seq:
        if re.search(regex, el):
            yield g
            g = []
        g.append(el)
    yield g

splitter = '^语文|数学|英语|科学|地理(.)*：'
level = '(^(语文|数学|英语)(博学|三层))|(科学|地理)(作业)?'
lines = re.findall(r'^(.+)(?:\n|\r\n?)', text, re.MULTILINE)
todo_list = list(group(lines, re.compile(splitter)))
my_todo_list = []
for todos in todo_list:
    if len(todos)>0 and re.match(level, todos[0]):
        my_todo_list.append(todos)

for todos in my_todo_list:
    for todo in todos:
        os.system(f'reminders add 作业 {todo}')

