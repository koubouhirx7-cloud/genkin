import glob
import re

html_files = glob.glob('*.html')
nav_map = {
    '入力': 'input_2.html',
    '履歴': 'history.html',
    '集計': 'summary.html',
    '設定': 'archive_summary.html'
}

for file in html_files:
    if file == 'login.html': continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add login redirect logic
    if "localStorage.getItem('app_logged_in')" not in content:
        head_end = content.find('</head>')
        if head_end != -1:
            script = "\n    <script>\n        if (localStorage.getItem('app_logged_in') !== 'true') {\n            window.location.href = 'login.html';\n        }\n    </script>\n"
            content = content[:head_end] + script + content[head_end:]
    
    # Replace '#' with correct HTML files mapping
    def repl(match):
        a_tag = match.group(0)
        for key, url in nav_map.items():
            if f">{key}</span>" in a_tag or f">{key}</p>" in a_tag or f">{key}<" in a_tag:
                return a_tag.replace('href="#"', f'href="{url}"')
        return a_tag
        
    content = re.sub(r'<a\s+[^>]*href="#"[^>]*>.*?</a>', repl, content, flags=re.DOTALL)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated HTML files.")
