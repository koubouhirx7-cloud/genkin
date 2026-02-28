// Script to be injected for PDF export functionality
async function exportToPDF() {
    const { jsPDF } = window.jspdf;
    
    // Create new A4 PDF
    const doc = new jsPDF({
        orientation: 'p',
        unit: 'mm',
        format: 'a4'
    });
    
    const records = JSON.parse(localStorage.getItem('cash_audit_records') || '[]');
    records.sort((a, b) => new Date(b.date) - new Date(a.date)); // Sort newest first
    
    if (records.length === 0) {
        alert("書き出す記録がありません。");
        return;
    }

    const recordsPerPage = 6; // 2 cols x 3 rows
    
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
    overlay.style.color = 'white';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.zIndex = '9999';
    overlay.innerHTML = '<div class="text-xl font-bold bg-white text-slate-900 p-6 rounded-2xl shadow-xl flex items-center gap-3"><span class="material-symbols-outlined animate-spin">refresh</span> PDFを作成中...</div>';
    document.body.appendChild(overlay);

    try {
        // Create an off-screen container for rendering A4 pages
        const renderContainer = document.createElement('div');
        renderContainer.style.width = '1122px'; // A4 width at 144 DPI
        renderContainer.style.padding = '40px';
        renderContainer.style.position = 'absolute';
        renderContainer.style.left = '-9999px';
        renderContainer.style.top = '0';
        renderContainer.style.backgroundColor = 'white';
        renderContainer.style.color = 'black';
        renderContainer.style.fontFamily = 'Inter, sans-serif';
        document.body.appendChild(renderContainer);

        const chunks = [];
        for (let i = 0; i < records.length; i += recordsPerPage) {
            chunks.push(records.slice(i, i + recordsPerPage));
        }

        let isFirstPage = true;

        for (const [pageIndex, chunk] of chunks.entries()) {
            renderContainer.innerHTML = ''; // Clear previous page
            
            // Header
            const header = document.createElement('div');
            header.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px;">
                    <h1 style="font-size: 32px; font-weight: bold; margin: 0;">現金実査 記録一覧</h1>
                    <span style="font-size: 16px; color: #666;">ページ ${pageIndex + 1} / ${chunks.length}</span>
                </div>
            `;
            renderContainer.appendChild(header);

            // Grid for 6 records (2 columns, 3 rows)
            const grid = document.createElement('div');
            grid.style.display = 'grid';
            grid.style.gridTemplateColumns = '1fr 1fr';
            grid.style.gap = '20px';
            
            for (const record of chunk) {
                const card = document.createElement('div');
                card.style.border = '1px solid #ccc';
                card.style.borderRadius = '12px';
                card.style.padding = '20px';
                card.style.display = 'flex';
                card.style.flexDirection = 'column';
                card.style.gap = '15px';
                
                const isBalanced = record.diff === 0;
                const statusColor = isBalanced ? '#059669' : '#DC2626';
                const statusBg = isBalanced ? '#D1FAE5' : '#FEE2E2';
                const statusText = isBalanced ? '一致 (±0)' : `不一致 (${record.diff > 0 ? '+' : ''}${record.diff.toLocaleString()})`;

                card.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 10px;">
                        <div>
                            <span style="font-size: 14px; color: #666;">実査日</span>
                            <div style="font-size: 20px; font-weight: bold;">${record.date.replace(/-/g, '/')}</div>
                        </div>
                        <div style="background-color: ${statusBg}; color: ${statusColor}; padding: 4px 12px; border-radius: 999px; font-size: 14px; font-weight: bold;">
                            ${statusText}
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <div style="flex: 1;">
                            <div style="font-size: 12px; color: #666;">実査日現金合計</div>
                            <div style="font-size: 24px; font-weight: bold;">¥${record.total.toLocaleString()}</div>
                        </div>
                        <div style="flex: 1; text-align: right;">
                            <div style="font-size: 12px; color: #666;">帳簿残高</div>
                            <div style="font-size: 20px; font-weight: bold; color: #444;">¥${record.ledger.toLocaleString()}</div>
                        </div>
                    </div>
                    <div style="margin-top: 10px; background: #f8f9fa; padding: 12px; border-radius: 8px; font-size: 14px; color: #444; min-height: 60px;">
                        <span style="font-size: 12px; color: #888; display: block; margin-bottom: 4px;">備考・過不足理由</span>
                        ${record.note ? record.note : '<span style="color: #bbb; font-style: italic;">（メモなし）</span>'}
                    </div>
                `;
                grid.appendChild(card);
            }
            
            renderContainer.appendChild(grid);

            // Render to canvas
            const canvas = await html2canvas(renderContainer, { scale: 1.5, useCORS: true });
            const imgData = canvas.toDataURL('image/jpeg', 0.9);
            
            if (!isFirstPage) {
                doc.addPage();
            }
            
            // Calculate height to maintain aspect ratio
            const imgProps = doc.getImageProperties(imgData);
            const pdfWidth = doc.internal.pageSize.getWidth();
            const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
            
            doc.addImage(imgData, 'JPEG', 0, 0, pdfWidth, pdfHeight);
            isFirstPage = false;
        }

        const dateStr = new Date().toISOString().split('T')[0];
        doc.save(`現金実査履歴_${dateStr}.pdf`);
        
        document.body.removeChild(renderContainer);
    } catch (error) {
        console.error("PDF Export Error: ", error);
        alert("PDFのエクスポート中にエラーが発生しました。");
    } finally {
        document.body.removeChild(overlay);
    }
}
window.exportToPDF = exportToPDF;
