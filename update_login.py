import glob

html_files = glob.glob('*.html')
script_block = """
    <script>
        if (localStorage.getItem('app_logged_in') !== 'true') {
            window.location.href = 'login.html';
        }
    </script>
"""

for f in html_files:
    if f == 'login.html': continue
    
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    if script_block in content:
        content = content.replace(script_block, '')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)

with open('login.html', 'r', encoding='utf-8') as f:
    login_content = f.read()

import re
new_script = """    <script>
        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const pass = document.getElementById('password').value;
            const btn = e.target.querySelector('button');
            const origText = btn.textContent;
            btn.textContent = '確認中...';
            btn.disabled = true;

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ pin: pass })
                });
                const data = await res.json();
                if(data.success) {
                    window.location.href = 'input_2.html';
                } else {
                    document.getElementById('error-msg').classList.remove('hidden');
                }
            } catch (err) {
                alert('サーバー通信に失敗しました (python3 server.py が起動しているか確認してください)');
            } finally {
                btn.textContent = origText;
                btn.disabled = false;
            }
        });
    </script>"""

login_content = re.sub(r'<script>.*?</script>', new_script, login_content, flags=re.DOTALL)
with open('login.html', 'w', encoding='utf-8') as f:
    f.write(login_content)

print("Updated login logic successfully")
