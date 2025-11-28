document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initSearch();
    initSort();
    // Chart is initialized when the analytics tab is first opened
});

/* Tabs */
function initTabs() {
    const buttons = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Deactivate all
            buttons.forEach(b => b.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            // Activate clicked
            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            const content = document.getElementById(tabId);
            if (content) {
                content.classList.add('active');
                if (tabId === 'analytics' && !window.chartRendered) {
                    renderChart();
                    window.chartRendered = true;
                }
            }
        });
    });
}

/* Search */
function initSearch() {
    const input = document.getElementById('tableSearch');
    if (!input) return;

    input.addEventListener('keyup', (e) => {
        const term = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(term) ? '' : 'none';
        });
    });
}

/* Sort */
function initSort() {
    const table = document.querySelector('table');
    if (!table) return;

    const headers = table.querySelectorAll('th');
    headers.forEach((header, index) => {
        header.addEventListener('click', () => {
            sortTable(table, index);
        });
    });
}

function sortTable(table, colIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isNumeric = colIndex === 0 || colIndex === 3; // Rank or Score
    const currentDir = table.getAttribute('data-sort-dir') === 'asc' ? 'desc' : 'asc';
    
    // Update sort direction
    table.setAttribute('data-sort-dir', currentDir);

    rows.sort((a, b) => {
        let valA = a.cells[colIndex].textContent.trim();
        let valB = b.cells[colIndex].textContent.trim();

        if (isNumeric) {
            valA = parseFloat(valA) || 0;
            valB = parseFloat(valB) || 0;
        }

        if (valA < valB) return currentDir === 'asc' ? -1 : 1;
        if (valA > valB) return currentDir === 'asc' ? 1 : -1;
        return 0;
    });

    rows.forEach(row => tbody.appendChild(row));
}

/* Chart */
// Note: renderChart function is defined in the HTML because it needs template variables
// We will expose a global function hook if needed, but for now the inline script in HTML 
// will call the library. However, to keep it clean, we can move the logic here if we pass data.
// For simplicity in this refactor, we'll keep the specific data injection in the HTML 
// but move the generic config here if possible. 
// Actually, let's keep the chart rendering in the HTML for now as it depends on Jinja2 variables,
// or we can fetch data via API. Given the current setup, passing data via a global variable is easiest.

window.drawChart = function(scoreRanges, fullMarksCount) {
    const dataPoints = [
        { label: "0-5", y: scoreRanges[0] },
        { label: "5-10", y: scoreRanges[1] },
        { label: "10-15", y: scoreRanges[2] },
        { label: "15-20", y: scoreRanges[3] },
        { label: "21 (العلامة الكاملة)", y: fullMarksCount }
    ];
    
    const chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "light2",
        backgroundColor: "transparent",
        title: {
            text: "توزيع النقاط",
            fontFamily: "El Messiri",
            fontSize: 24,
            fontColor: "#4a0072"
        },
        axisX: {
            title: "النقطة",
            titleFontFamily: "El Messiri",
            labelFontFamily: "El Messiri",
            gridThickness: 0
        },
        axisY: {
            title: "عدد المشاركين",
            includeZero: true,
            titleFontFamily: "El Messiri",
            labelFontFamily: "El Messiri",
            gridColor: "rgba(0,0,0,0.05)"
        },
        data: [{
            type: "column",
            color: "#7b1fa2",
            dataPoints: dataPoints,
            indexLabelFontFamily: "El Messiri",
            indexLabelFontColor: "#333",
            indexLabelFontSize: 14,
            indexLabel: "{y}"
        }]
    });
    chart.render();
};
