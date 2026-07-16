def fix():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The issue is exactly this literal string replacing what was there:
    bad_part = """+'<button class="rolebtn" onclick="pickRole(\\'director\\')"><span class="ic">&#127963;</span>Director Login</button>\\'
</div>';"""
    
    # Wait, the exact text in the file is:
    # +'<button class="rolebtn" onclick="pickRole(\'director\')"><span class="ic">&#127963;</span>Director Login</button>'
    # </div>';
    
    # Let's just use regex to fix `\n</div>';` that doesn't have a `+` in front of it in the renderLogin function.
    import re
    html = re.sub(r"(Director Login</button>')\n</div>';", r"\1\n+'</div>';", html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix()
