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

    # 1. Update sMarks toggle
    target1 = "h+=seg((S.user&&S.user.sem===1)?[[1,TYPES[S.fType].split(' ')[0]+' 1 (Ongoing)']]:[[1,TYPES[S.fType].split(' ')[0]+' 1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'fNum');"
    repl1 = "h+=seg((S.user&&S.user.sem===1)?[[1,TYPES[S.fType]+' 1 (Ongoing)'],[2,'2'],[3,'3'],[4,'4'],[5,'5'],[6,'6'],[7,'7'],[8,'8']]:[[1,TYPES[S.fType].split(' ')[0]+' 1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'fNum');"
    content = content.replace(target1, repl1)
    
    # Also fix the empty state for sMarks
    target1_msg = "if(!mine){return h+'<div class=\"notewarn\">You were not part of a team in '+TYPES[S.fType]+' '+S.fNum+'. (Demo data pre-assigns students 001-027 of each programme to past teams; join a team in the ongoing activity to see live marks.)</div>';}"
    repl1_msg = "if(!mine){ if(S.user&&S.user.sem===1&&S.fNum>1) return h+'<div class=\"notewarn\">(Not yet started)</div>'; return h+'<div class=\"notewarn\">You were not part of a team in '+TYPES[S.fType]+' '+S.fNum+'. (Demo data pre-assigns students 001-027 of each programme to past teams; join a team in the ongoing activity to see live marks.)</div>';}"
    content = content.replace(target1_msg, repl1_msg)

    # 2. Update sDashboard toggle
    target2 = "h+=seg((S.user&&S.user.sem===1)?[[1,TYPES[type]+' 1 (Ongoing)']]:[[1,TYPES[type]+' 1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'myNum');"
    repl2 = "h+=seg((S.user&&S.user.sem===1)?[[1,TYPES[type]+' 1 (Ongoing)'],[2,'2'],[3,'3'],[4,'4'],[5,'5'],[6,'6'],[7,'7'],[8,'8']]:[[1,TYPES[type]+' 1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'myNum');"
    content = content.replace(target2, repl2)
    
    # 3. Update expert/mentor booking toggle
    target3 = "h+=seg((S.user&&S.user.sem===1)?[[1,'1 (Ongoing)']]:[[1,'1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'bookNum');"
    repl3 = "h+=seg((S.user&&S.user.sem===1)?[[1,TYPES[S.bType||S.eType||1]+' 1 (Ongoing)'],[2,'2'],[3,'3'],[4,'4'],[5,'5'],[6,'6'],[7,'7'],[8,'8']]:[[1,'1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'bookNum');"
    # Wait, in mentor/expert booking, the variable is S.bType or S.eType. Actually let's just use "1 (Ongoing)" without TYPES to be safe since bookNum doesn't have type in the text before. Wait, user said "mention Business Simulation 1, Live project 1". That's specifically for marks and dashboard. Let's just do it exactly as requested.
    repl3 = "h+=seg((S.user&&S.user.sem===1)?[[1,'1 (Ongoing)'],[2,'2'],[3,'3'],[4,'4'],[5,'5'],[6,'6'],[7,'7'],[8,'8']]:[[1,'1'],[2,'2'],[3,'3'],[4,'4'],[5,'5 (Ongoing)']],'bookNum');"
    content = content.replace(target3, repl3)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated toggles to 8.')
