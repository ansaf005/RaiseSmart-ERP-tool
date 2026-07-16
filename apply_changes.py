import re

def apply_all():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Colors in sActivity
    # Find the line: h+='<div class="card" style="'+(st==='Not Yet Started'&&!pubQ?'opacity:.55;background:var(--bg)':'')+'">'+body+'</div>';
    html = html.replace(
        """h+='<div class="card" style="'+(st==='Not Yet Started'&&!pubQ?'opacity:.55;background:var(--bg)':'')+'">'+body+'</div>';""",
        """h+='<div class="card" style="'+(st==='Completed'?'background:#e5e7eb':(st==='Ongoing'?'background:#e6f7f1;border-color:#0e9f6e':'opacity:.6;background:#fff'))+'">'+body+'</div>';"""
    )
    # Also fix semester 1 dummy cards loop logic if needed, but the main logic is handled above.
    html = html.replace(
        """for(var n2=2;n2<=8;n2++){h1+='<div class="card" style="opacity:.55;background:var(--bg)"><h3>'+TYPES[type]+' '+n2+'</h3><div class="sub" style="margin-bottom:8px">Semester '+semOf(n2)+'</div>'+statusChip('x')+'</div>';}""",
        """for(var n2=2;n2<=8;n2++){h1+='<div class="card" style="opacity:.6;background:#fff"><h3>'+TYPES[type]+' '+n2+'</h3><div class="sub" style="margin-bottom:8px">Semester '+semOf(n2)+'</div>'+statusChip('x')+'</div>';}"""
    )

    # 2. Marks out of 100 in sMarks
    # Replace the total / maxT logic
    html = html.replace(
        """+'<div class="stat"><div class="n">'+total+' / '+maxT+'</div><div class="l">Overall team mark ('+mine.team.team+')</div></div></div>'""",
        """+'<div class="stat"><div class="n">'+(maxT?Math.round((total/maxT)*100):0)+' / 100</div><div class="l">Overall team mark ('+mine.team.team+')</div></div></div>'"""
    )

    # 3. Terminology: Question/Problem -> Challenge
    html = html.replace("Problem statement choosing", "Challenge choosing")
    html = html.replace("Problem Statement choosing", "Challenge choosing")
    html = html.replace("Problem Statement", "Challenge")
    html = html.replace("Problem Statements", "Challenges")
    html = html.replace("problem statement", "challenge")
    html = html.replace("problem statements", "challenges")
    html = html.replace("Problem posting", "Challenge posting")
    html = html.replace("Question posting", "Challenge posting")
    html = html.replace("question posting", "challenge posting")
    
    # "Preview Problem Statements" button in sActivity
    html = html.replace("Preview Problem Statements", "Preview Challenges")

    # 4. Director Approvals for Choosing & Booking
    # Let's add auth flags to `evalAuth` logic.
    # Where does it check auth for choosing? 
    # In `sActivity` (ongoing state)
    #   if(st==='Ongoing'){body+='<div style="margin-top:12px"><button class="btn" onclick="S.chooseKey=\''+actKey(type,n,S.user.campus)+'\';if(window.syncState) window.syncState(); go(S.tab)">Choose the Challenge &rarr;</button></div>';}
    # We change it to check S.evalAuth.chooseAppr
    html = html.replace(
        """if(st==='Ongoing'){body+='<div style="margin-top:12px"><button class="btn" onclick="S.chooseKey=\\''+actKey(type,n,S.user.campus)+'\\';if(window.syncState) window.syncState(); go(S.tab)">Choose the Challenge &rarr;</button></div>';}""",
        """if(st==='Ongoing'){
            if(S.evalAuth.chooseAppr) body+='<div style="margin-top:12px"><button class="btn" onclick="S.chooseKey=\\''+actKey(type,n,S.user.campus)+'\\';if(window.syncState) window.syncState(); go(S.tab)">Choose the Challenge &rarr;</button></div>';
            else body+='<div class="noteinfo" style="margin-top:12px">Challenge choosing is locked by Director.</div>';
        }"""
    )
    
    # Mentor booking auth: in `tlGate` (it applies to both mentors and experts usually, but they specifically mentioned "expert booking")
    # Actually wait, "for expert booking... once director gives permission...". 
    # Let's find `bookExpert` or `sExpert`.
    # Let's inject a check at the top of `sExpert`:
    # if(!S.evalAuth.expertAppr) return '<h2>Review Expert Booking</h2><div class="notewarn">Expert booking is currently locked by the Director.</div>';
    html = re.sub(
        r"function sExpert\(\)\{",
        r"function sExpert(){ if(!S.evalAuth.expertAppr) return '<h2>Review Expert Booking</h2><div class=\"notewarn\">Expert booking is currently locked by the Director.</div>';",
        html
    )

    # Add the toggle buttons for Director in `dEvalCtl()`
    # Let's find `dEvalCtl()` and add them.
    # We can just add them right next to other toggles.
    # Wait, the prototype has `function dEvalCtl(){...}`. Let's see what's in it using regex, or simply append our toggles to the HTML returned by it.
    html = re.sub(
        r"(function dEvalCtl\(\)\{.*?'</div>';\n\})",
        lambda m: m.group(1).replace(
            "return h+'</div>';", 
            "h+='<h3>Global Approvals</h3><div class=\"grid2\">' + "
            "('<div class=\"card\" style=\"display:flex;align-items:center;justify-content:space-between\"><b>Challenge Choosing</b> ' + (S.evalAuth.chooseAppr?'<button class=\"btnr\" onclick=\"S.evalAuth.chooseAppr=false;if(window.syncState) window.syncState(); go(\\'deval\\')\">Lock</button>':'<button class=\"btng\" onclick=\"S.evalAuth.chooseAppr=true;if(window.syncState) window.syncState(); go(\\'deval\\')\">Approve (Unlock)</button>') + '</div>') + "
            "('<div class=\"card\" style=\"display:flex;align-items:center;justify-content:space-between\"><b>Expert Booking</b> ' + (S.evalAuth.expertAppr?'<button class=\"btnr\" onclick=\"S.evalAuth.expertAppr=false;if(window.syncState) window.syncState(); go(\\'deval\\')\">Lock</button>':'<button class=\"btng\" onclick=\"S.evalAuth.expertAppr=true;if(window.syncState) window.syncState(); go(\\'deval\\')\">Approve (Unlock)</button>') + '</div>') + '</div>'; "
            "return h+'</div>';"
        ),
        html, flags=re.DOTALL
    )

    # 5. Publish Buttons Text
    html = html.replace(">Overall Publish<", ">Publish<")
    html = html.replace(">Publish All Marks<", ">Publish<")
    html = html.replace(">Publish Marks<", ">Publish<")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Done")

if __name__ == '__main__':
    apply_all()
