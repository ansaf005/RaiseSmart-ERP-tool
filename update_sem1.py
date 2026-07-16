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

    # 1. Fix sMarks
    # h+=seg([[1,TYPES[S.fType].split(' ')[0]+' 1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'fNum');
    target1 = "h+=seg([[1,TYPES[S.fType].split(' ')[0]+' 1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'fNum');"
    repl1 = "if(S.user&&S.user.sem===1&&S.fNum!=1)S.fNum=1; h+=seg((S.user&&S.user.sem===1)?[[1,TYPES[S.fType].split(' ')[0]+' 1 (Ongoing)']]:[[1,TYPES[S.fType].split(' ')[0]+' 1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'fNum');"
    content = content.replace(target1, repl1)

    # 2. Fix sDashboard
    # h+=seg([[1,TYPES[type]+' 1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'myNum');
    target2 = "h+=seg([[1,TYPES[type]+' 1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'myNum');"
    repl2 = "if(S.user&&S.user.sem===1&&S.myNum!=1)S.myNum=1; h+=seg((S.user&&S.user.sem===1)?[[1,TYPES[type]+' 1 (Ongoing)']]:[[1,TYPES[type]+' 1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'myNum');"
    content = content.replace(target2, repl2)

    # 3. Fix expert booking and mentor booking
    # h+=seg([[1,'1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'bookNum');
    target3 = "h+=seg([[1,'1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'bookNum');"
    repl3 = "if(S.user&&S.user.sem===1&&S.bookNum!=1)S.bookNum=1; h+=seg((S.user&&S.user.sem===1)?[[1,'1 (Ongoing)']]:[[1,'1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'bookNum');"
    content = content.replace(target3, repl3)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated semester UI logic.')
