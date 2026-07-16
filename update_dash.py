import os
import re

files = [
    'c:\\Users\\ansaf\\OneDrive\\Desktop\\RSmart-ERP-Portal.html 2.html',
    'c:\\Users\\ansaf\\OneDrive\\Desktop\\R-SMART ERP PORTAL\\index.html',
    'c:\\Users\\ansaf\\OneDrive\\Desktop\\R-SMART ERP PORTAL\\index.js',
    'c:\\Users\\ansaf\\OneDrive\\Desktop\\R-SMART ERP PORTAL\\script.js'
]

for fp in files:
    if not os.path.exists(fp):
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change condition for BS 1 / LP 1
    content = content.replace("(S.user.sem===1?'BS 1 / LP 1':'BS 5 / LP 5')", "(S.user.sem<=2?'BS 1 / LP 1':'BS 5 / LP 5')")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated dashboard ongoing text.')
