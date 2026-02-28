import re

with open('input_2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace all non-zero value attributes in number inputs for cash
pattern = r'(<input class="w-12 text-center border-none bg-transparent font-bold text-lg focus:ring-0 p-0"\s*type="number" value=")\d+(" />)'
content = re.sub(pattern, r'\g<1>0\g<2>', content)

# 2. Remove Ledger Balance Input
ledger_input_section = """        <!-- Ledger Balance Input -->
        <div class="p-4 mt-2 border-t border-slate-100 dark:border-slate-800">
            <label class="block text-xs font-bold text-slate-500 dark:text-slate-400 mb-2">帳簿残高</label>
            <div class="relative">
                <span class="absolute left-3 top-1/2 -translate-y-1/2 font-bold text-slate-500">¥</span>
                <input type="number" id="ledger-input"
                    class="w-full pl-8 py-3 rounded-xl border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/40 text-lg font-bold focus:border-primary focus:ring-primary"
                    value="162148">
            </div>
        </div>"""
content = content.replace(ledger_input_section, "")

# 3. Remove Difference from Footer
diff_footer_section = """                <div
                    class="bg-slate-50 dark:bg-slate-800/50 p-3 rounded-xl border border-slate-100 dark:border-slate-800">
                    <p class="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1">
                        帳簿残高との差</p>
                    <div class="flex items-center gap-1">
                        <p class="text-lg font-bold text-emerald-500">±0</p>
                        <span class="material-symbols-outlined text-emerald-500 text-sm">check_circle</span>
                    </div>
                </div>"""
content = content.replace(diff_footer_section, "")

# Also the footer is currently grid-cols-2. Make it grid-cols-1 or leave it if it shrinks nicely. Let's make it grid-cols-1
content = content.replace('class="grid grid-cols-2 gap-4"', 'class="grid grid-cols-1 gap-4"')

# 4. Remove Javascript logic corresponding to ledger
js_ledger_1 = """            const diffEl = document.querySelectorAll('footer .text-lg.font-bold')[1];
            const ledgerInput = document.getElementById('ledger-input');
            let diffIcon = null;
            if (diffEl) {
                diffIcon = diffEl.nextElementSibling;
            }"""
content = content.replace(js_ledger_1, "")

js_ledger_2 = """                const ledger = parseInt(ledgerInput.value) || 0;
                if (diffEl) {
                    const diff = currentTotal - ledger;
                    if (diff === 0) {
                        diffEl.textContent = '±0';
                        diffEl.className = 'text-lg font-bold text-emerald-500';
                        if (diffIcon) {
                            diffIcon.textContent = 'check_circle';
                            diffIcon.className = 'material-symbols-outlined text-emerald-500 text-sm';
                        }
                    } else {
                        diffEl.textContent = `${diff > 0 ? '+' : ''}${diff.toLocaleString()}`;
                        diffEl.className = 'text-lg font-bold text-rose-500';
                        if (diffIcon) {
                            diffIcon.textContent = 'warning';
                            diffIcon.className = 'material-symbols-outlined text-rose-500 text-sm';
                        }
                    }
                }"""
content = content.replace(js_ledger_2, "")

js_ledger_3 = """            if (ledgerInput) {
                ledgerInput.addEventListener('input', update);
            }"""
content = content.replace(js_ledger_3, "")


js_ledger_4 = """                    if (ledgerInput) ledgerInput.value = currentRecord.ledger;"""
content = content.replace(js_ledger_4, "")

js_ledger_5 = """                    const ledgerVal = parseInt(ledgerInput.value) || 0;
                    const noteStr = document.getElementById('audit-note').value;
                    const diffVal = currentTotalVal - ledgerVal;"""
content = content.replace(js_ledger_5, """                    const ledgerVal = 0;
                    const noteStr = document.getElementById('audit-note').value;
                    const diffVal = 0;""")


with open('input_2.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("done")
