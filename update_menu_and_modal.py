import glob
import re

html_files = ['input_2.html', 'history.html', 'summary.html', 'archive_summary.html']

menu_and_modal_html = """
    <!-- Hamburger Menu -->
    <div id="mobile-menu" class="hidden fixed inset-0 z-[100]">
        <div class="absolute inset-0 bg-black/20 backdrop-blur-sm" onclick="document.getElementById('mobile-menu').classList.add('hidden')"></div>
        <div class="absolute top-16 right-4 w-56 bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden py-2" id="mobile-menu-content">
            <a href="input_2.html" class="flex items-center gap-3 px-4 py-3 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                <span class="material-symbols-outlined text-[20px]">add_box</span>
                <span class="font-medium text-sm">入力</span>
            </a>
            <a href="history.html" class="flex items-center gap-3 px-4 py-3 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                <span class="material-symbols-outlined text-[20px]">history</span>
                <span class="font-medium text-sm">履歴</span>
            </a>
            <a href="summary.html" class="flex items-center gap-3 px-4 py-3 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                <span class="material-symbols-outlined text-[20px]">bar_chart</span>
                <span class="font-medium text-sm">集計</span>
            </a>
            <div class="h-px bg-slate-100 dark:bg-slate-800 my-1 mx-4"></div>
            <a href="archive_summary.html" class="flex items-center gap-3 px-4 py-3 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                <span class="material-symbols-outlined text-[20px]">settings</span>
                <span class="font-medium text-sm">設定・アーカイブ</span>
            </a>
        </div>
    </div>
"""

delete_modal_html = """
    <!-- Delete Confirm Modal -->
    <div id="delete-modal" class="hidden fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity" onclick="closeDeleteModal()"></div>
        <div class="bg-white dark:bg-slate-900 rounded-2xl shadow-xl max-w-sm w-full p-6 relative z-10 scale-100 transition-transform">
            <div class="w-12 h-12 rounded-full bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 flex items-center justify-center mb-4 mx-auto">
                <span class="material-symbols-outlined text-[24px]">warning</span>
            </div>
            <h3 class="text-lg font-bold text-center text-slate-900 dark:text-white mb-2">記録の削除</h3>
            <p class="text-sm text-center text-slate-500 dark:text-slate-400 mb-6">この記録を削除してもよろしいですか？<br>この操作は取り消せません。</p>
            <div class="flex gap-3">
                <button onclick="closeDeleteModal()" class="flex-1 py-3 px-4 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl font-bold hover:bg-slate-200 transition-colors">キャンセル</button>
                <button id="confirm-delete-btn" class="flex-1 py-3 px-4 bg-red-600 hover:bg-red-700 text-white rounded-xl font-bold shadow-lg shadow-red-600/30 transition-colors">削除する</button>
            </div>
        </div>
    </div>
"""

def inject_html(file, append_html):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'id="mobile-menu"' not in content:
        content = content.replace("</body>", append_html + "\n</body>")
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

# Inject into all
for f in html_files:
    if f == 'history.html':
        inject_html(f, menu_and_modal_html + delete_modal_html)
    else:
        inject_html(f, menu_and_modal_html)

# Add headers
def replace_in_file(filename, old, new):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

# input_2.html
replace_in_file('input_2.html',
    '<span class="material-symbols-outlined text-slate-600 dark:text-slate-400 cursor-pointer" onclick="window.location.href=\'history.html\'">history</span>',
    '<span class="material-symbols-outlined text-slate-600 dark:text-slate-400 cursor-pointer" onclick="window.location.href=\'history.html\'">history</span>\n                <span class="material-symbols-outlined text-slate-600 dark:text-slate-400 cursor-pointer" onclick="document.getElementById(\'mobile-menu\').classList.remove(\'hidden\')">menu</span>')

# history.html
h_old_str = """            <button class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors" onclick="window.location.href='archive_summary.html'">
                <span class="material-symbols-outlined text-slate-600 dark:text-slate-400">calendar_month</span>
            </button>"""
h_new_str = """            <div class="flex items-center gap-1">
                <button class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors" onclick="window.location.href='archive_summary.html'">
                    <span class="material-symbols-outlined text-slate-600 dark:text-slate-400">calendar_month</span>
                </button>
                <button class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors" onclick="document.getElementById('mobile-menu').classList.remove('hidden')">
                    <span class="material-symbols-outlined text-slate-600 dark:text-slate-400">menu</span>
                </button>
            </div>"""
replace_in_file('history.html', h_old_str, h_new_str)

# summary.html
s_old_str = """            <h2
                class="text-slate-900 dark:text-slate-100 text-lg font-bold leading-tight tracking-tight flex-1 text-center pr-10">
                集計画面</h2>
        </div>"""
s_new_str = """            <h2 class="text-slate-900 dark:text-slate-100 text-lg font-bold leading-tight tracking-tight flex-1 text-center">集計画面</h2>
            <div onclick="document.getElementById('mobile-menu').classList.remove('hidden')" class="text-primary flex size-10 shrink-0 items-center justify-center rounded-full hover:bg-primary/10 cursor-pointer">
                <span class="material-symbols-outlined">menu</span>
            </div>
        </div>"""
replace_in_file('summary.html', s_old_str, s_new_str)

# archive_summary.html
a_old_str = """<div class="w-10"></div> <!-- Spacer for centering -->"""
a_new_str = """<button class="flex items-center justify-center p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" onclick="document.getElementById('mobile-menu').classList.remove('hidden')">
            <span class="material-symbols-outlined text-slate-600 dark:text-slate-400">menu</span>
        </button>"""
replace_in_file('archive_summary.html', a_old_str, a_new_str)


# history.html delete script
with open('history.html', 'r', encoding='utf-8') as f:
    content = f.read()

del_script_find = """btn.addEventListener('click', (e) => {
                        if (confirm('この記録を削除してもよろしいですか？')) {
                            const id = e.currentTarget.getAttribute('data-id');
                            let recs = loadRecords();
                            recs = recs.filter(r => r.id !== id);
                            saveRecords(recs);
                            renderRecords();
                        }
                    });"""

del_script_replace = """btn.addEventListener('click', (e) => {
                        e.preventDefault();
                        e.stopPropagation(); // prevent window location change
                        const id = e.currentTarget.getAttribute('data-id');
                        const modal = document.getElementById('delete-modal');
                        modal.classList.remove('hidden');
                        
                        const confirmBtn = document.getElementById('confirm-delete-btn');
                        
                        // Clear old listeners
                        const newConfirmBtn = confirmBtn.cloneNode(true);
                        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
                        
                        newConfirmBtn.addEventListener('click', () => {
                            let recs = loadRecords();
                            recs = recs.filter(r => r.id !== id);
                            saveRecords(recs);
                            renderRecords();
                            closeDeleteModal();
                        });
                    });"""

close_modal_func = """
            window.closeDeleteModal = function() {
                document.getElementById('delete-modal').classList.add('hidden');
            };
"""

if del_script_find in content:
    content = content.replace(del_script_find, del_script_replace)
    # Add closeModalFunc inside script block
    content = content.replace("function loadRecords()", close_modal_func + "\n            function loadRecords()")
    with open('history.html', 'w', encoding='utf-8') as f:
        f.write(content)

print("Menu and custom modal injected successfully.")
