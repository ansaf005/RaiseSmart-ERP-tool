import os

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

    # We previously injected: S.user&&S.user.sem===1
    content = content.replace("S.user&&S.user.sem===1", "S.user&&S.user.sem<=2")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated S.user.sem<=2 for all first year students.')
