import re

def apply_theme():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Change root variables
    # Old: :root{--p:#1a56db;--pl:#eaf1fd;--pd:#0f3e9e;--gold:#c9920e;--goldl:#fdf6e3;--green:#0e9f6e;--greenl:#e6f7f1;--red:#d92626;--redl:#fdeaea;--amber:#c27803;--amberl:#fdf3e3;--ink:#1f2a37;--mut:#6b7280;--line:#e5e7eb;--bg:#f8fafc}
    html = re.sub(
        r':root\{.*?\}',
        ':root{--p:#8e24aa;--pl:#f3e5f5;--pd:#6a1b9a;--gold:#c9920e;--goldl:#fdf6e3;--green:#0e9f6e;--greenl:#e6f7f1;--red:#d92626;--redl:#fdeaea;--amber:#f57c00;--amberl:#fff3e0;--ink:#1f2a37;--mut:#6b7280;--line:#e5e7eb;--bg:#f8fafc}',
        html
    )

    # Change .logo CSS to match an image if needed, but it's better to just replace the div with an img tag
    # In nav bar (assumed to be something like <div class="logo"...>R</div>)
    # We will just replace all `<div class="logo"[^>]*>R</div>` with `<img src="logo.png" style="height:36px; object-fit:contain" />`
    # For login screen: `<div class="logo" style="margin:0 auto 12px;width:56px;height:56px;font-size:26px">R</div>` -> `<img src="logo.png" style="height:60px; margin:0 auto 12px; display:block; object-fit:contain" />`
    
    html = re.sub(
        r'<div class="logo" style="margin:0 auto 12px;[^>]*>R</div>',
        '<img src="logo.png" style="height:60px; margin:0 auto 12px; display:block; object-fit:contain" />',
        html
    )
    
    html = re.sub(
        r'<div class="logo"[^>]*>R</div>',
        '<img src="logo.png" style="height:32px; margin-right:8px; object-fit:contain" />',
        html
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Theme applied")

if __name__ == '__main__':
    apply_theme()
