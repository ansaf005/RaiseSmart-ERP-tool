import re

def update_login():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove demo credentials block
    demo_block = r"\\+'<div class=\"demo\"><b>Demo credentials</b>.*?</div>';"
    html = re.sub(demo_block, "';", html, flags=re.DOTALL)

    # 2. Remove Admin button from rolegrid
    admin_btn = r"\\+'<button class=\"rolebtn\" onclick=\"pickRole\(\\'admin\\'\)\"><span class=\"ic\">&#9881;</span>Admin Login</button>'"
    html = re.sub(admin_btn, "", html)

    # 3. Add Admin button to top right
    # We will inject it inside the <div class="login-wrap">
    # The code currently does: el.innerHTML='<div class="login-wrap"><div class="login-card">'+inner+'</div></div>';
    admin_top_right = """<div style="position:absolute; top:20px; right:20px;"><button class="btn2" style="background:rgba(255,255,255,0.8); border:none; box-shadow:0 2px 8px rgba(0,0,0,0.1);" onclick="pickRole(\\'admin\\')">&#9881; Admin Login</button></div>"""
    
    html = html.replace(
        """el.innerHTML='<div class="login-wrap"><div class="login-card">'+inner+'</div></div>';""",
        f"""el.innerHTML='{admin_top_right}<div class="login-wrap"><div class="login-card">'+inner+'</div></div>';"""
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    update_login()
