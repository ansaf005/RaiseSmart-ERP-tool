import sys
import re

html = open('index.js', encoding='utf-8').read()

funcs = ['sActivity', 'sChoose', 'dStudentMarks', 'marksTableFor', 'aStudentMarks', 'sMarks', 'buildStudentCharts']
out = open('funcs.txt', 'w', encoding='utf-8')

for func in funcs:
    idx = html.find('function ' + func + '(')
    if idx == -1: continue
    braces = 0
    in_str = False
    str_char = ''
    i = idx
    while i < len(html):
        c = html[i]
        if in_str:
            if c == '\\': i += 1
            elif c == str_char: in_str = False
        elif c in ['\'', '"', '`']:
            in_str = True
            str_char = c
        elif c == '{': braces += 1
        elif c == '}':
            braces -= 1
            if braces == 0:
                out.write(html[idx:i+1] + '\n\n')
                break
        i += 1
out.close()
