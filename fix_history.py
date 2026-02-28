import re

with open('history.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the '一致', '不一致', '過去30日' filter buttons section
filter_section = """            <!-- Horizontal Scroll Filters -->
            <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                <button
                    class="flex items-center gap-1.5 px-4 py-2 bg-primary text-white rounded-full text-sm font-medium whitespace-nowrap shadow-sm shadow-primary/20">
                    すべて
                </button>
                <button
                    class="flex items-center gap-1.5 px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 rounded-full text-sm font-medium whitespace-nowrap hover:bg-slate-50">
                    一致
                    <span class="material-symbols-outlined text-xs">keyboard_arrow_down</span>
                </button>
                <button
                    class="flex items-center gap-1.5 px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 rounded-full text-sm font-medium whitespace-nowrap hover:bg-slate-50">
                    不一致
                    <span class="material-symbols-outlined text-xs">keyboard_arrow_down</span>
                </button>
                <button
                    class="flex items-center gap-1.5 px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 rounded-full text-sm font-medium whitespace-nowrap hover:bg-slate-50">
                    過去30日
                    <span class="material-symbols-outlined text-xs">keyboard_arrow_down</span>
                </button>
            </div>"""

content = content.replace(filter_section, "")

# Remove Javascript filter logic
js_filter_1 = """                    let matchesFilter = true;
                    if (currentFilter === '一致') {
                        matchesFilter = isBalanced;
                    } else if (currentFilter === '不一致') {
                        matchesFilter = !isBalanced;
                    } else if (currentFilter === '過去30日') {
                        const diffDays = (new Date() - new Date(record.date)) / (1000 * 60 * 60 * 24);
                        matchesFilter = diffDays <= 30;
                    }

                    if (!matchesSearch || !matchesFilter) return;"""

js_filter_replace_1 = """                    if (!matchesSearch) return;"""

content = content.replace(js_filter_1, js_filter_replace_1)

# Remove the status text generation and icons
js_status_gen = """                    const isBalanced = record.diff === 0;
                    const statusText = isBalanced ? '一致' : `不一致 (${record.diff > 0 ? '+' : ''}¥${record.diff.toLocaleString()})`;
                    // Convert YYYY-MM-DD to cleaner format depending on structure
                    const displayDate = record.date.replace(/-/g, '/');
                    const searchStr = `${displayDate} ${statusText}`.toLowerCase();"""

js_status_gen_replace = """                    const displayDate = record.date.replace(/-/g, '/');
                    const searchStr = `${displayDate}`.toLowerCase();"""

content = content.replace(js_status_gen, js_status_gen_replace)

js_icon_gen = """                    const iconClass = isBalanced ? 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30' : 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30';
                    const iconName = isBalanced ? 'check_circle' : 'warning';
                    const statusColor = isBalanced ? 'text-slate-500 dark:text-slate-400' : 'text-red-500 font-medium';"""

js_icon_gen_replace = """                    const iconClass = 'text-primary bg-primary/10';
                    const iconName = 'receipt_long';"""

content = content.replace(js_icon_gen, js_icon_gen_replace)

# Remove the statusText output in HTML template
card_html_seek = """                                <div>
                                    <p class="font-bold text-slate-900 dark:text-slate-100">${displayDate}</p>
                                    <p class="text-sm ${statusColor}">${statusText}</p>
                                </div>"""

card_html_replace = """                                <div>
                                    <p class="font-bold text-slate-900 dark:text-slate-100">${displayDate}</p>
                                </div>"""

content = content.replace(card_html_seek, card_html_replace)

with open('history.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("done history fixing")
