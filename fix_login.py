def fix():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    bad_text = """+'<button class="rolebtn" onclick="pickRole(\\'admin\\')"><span class="ic">&#9881;</span>Admin Login</button></div>'
+'<div class="demo"><b>Demo credentials</b> (prototype - data resets on refresh)<br>'
+'&#8226; Student (free, can choose a team): <b>RTC26MBA028</b> / <b>Echo@1999</b> &nbsp;|&nbsp; RGU: <b>RGU26MBA028</b> / <b>Echo@3183</b><br>'
+'&#8226; Student (already in Team 1, sees marks): <b>RTC26MBA001</b> / <b>Nova@1000</b><br>'
+'&#8226; NEW 1st-year student (Semester 1 - picks any specializations): <b>RTC27MBA001</b> / <b>Fresh@2001</b><br>'
+'&#8226; Mark Entry now needs Director approval: Director &rarr; Evaluation Control &rarr; Approve &amp; Start.<br>'
+'&#8226; Coordinator: <b>COORD</b> / <b>Coord@2026</b> &nbsp;&#8226; Director: <b>DIRECTOR</b> / <b>Direct@2026</b> &nbsp;&#8226; Admin: <b>ADMIN</b> / <b>Admin@2026</b><br>'
+'&#8226; Full list of all 64 student passwords: Admin login &rarr; Credentials tab.</div>';"""

    if bad_text in html:
        html = html.replace(bad_text, "</div>';")
        print("Success replacing block.")
    else:
        print("Could not find the block.")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix()
