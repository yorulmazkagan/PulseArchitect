let lastProcessedTimestamp = 0; 
let myChart;

window.onload = async () => { 
    console.log("PulseArchitect Initializing...");
    await refreshAll(); 
};

async function refreshAll() {
    try {
        const resp = await fetch('http://127.0.0.1:8000/activities');
        const logs = await resp.json();
        if (logs.length === 0) return;

        const sorted = logs.sort((a, b) => b.timestamp - a.timestamp);
        const chatBox = document.getElementById('chatBox');
        
        chatBox.innerHTML = sorted.map(l => `
            <div class="activity-log p-4 border-l-4 border-yellow-500 bg-yellow-900/20 mb-4 rounded">
                <p class="neon-text-gold font-bold italic text-sm">⚡ [SYSTEM MEMORY]</p>
                <p class="text-white text-xs leading-relaxed opacity-90">${l.answer || 'No analysis data found.'}</p>
            </div>`).join('') + '<div class="text-red-500 font-bold">>>> PulseArchitect Sovereign Mode Active.</div>';

        updateDashboard(sorted[0]);
        updateChart(logs);
        updateGear(sorted[0]);
        lastProcessedTimestamp = sorted[0].timestamp;
    } catch (err) { 
        console.error("Error:", err); 
    }
}

setInterval(async () => {
    try {
        const activityResp = await fetch('http://127.0.0.1:8000/activities');
        const activities = await activityResp.json();
        
        if (activities.length > 0) {
            const sorted = activities.sort((a, b) => b.timestamp - a.timestamp);
            const latest = sorted[0];

            if (latest.timestamp !== lastProcessedTimestamp) {
                const chatBox = document.getElementById('chatBox');
                chatBox.insertAdjacentHTML('afterbegin', `
                    <div class="activity-log p-4 border-l-4 border-yellow-500 bg-yellow-900/20 mb-4 rounded animate-pulse">
                        <p class="neon-text-gold font-bold italic text-sm">⚡ [NEW AUTONOMOUS ANALYSIS]</p>
                        <p class="text-white text-xs leading-relaxed opacity-90">${latest.answer}</p>
                    </div>`);
                
                if (chatBox.children.length > 7) chatBox.removeChild(chatBox.lastChild);

                lastProcessedTimestamp = latest.timestamp;
                updateDashboard(latest);
                updateChart(activities);
                updateGear(latest);
            }
        }
        loadTickets(); 
    } catch (err) { 
        console.warn("Synchronization pending..."); 
    }
}, 5000);

async function askAgent() {
    const input = document.getElementById('userInput');
    const msg = input.value;
    if (!msg) return;

    document.getElementById('chatBox').insertAdjacentHTML('afterbegin', `<div class="mb-4 text-yellow-500"><strong>User:</strong> ${msg}</div>`);
    input.value = '';

    try {
        const response = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await response.json();
        updateDashboard(data.metrics ? data : { metrics: data.metrics }); 
        document.getElementById('chatBox').insertAdjacentHTML('afterbegin', `<div class="mb-4 text-green-400"><strong>Agent:</strong> ${data.answer}</div>`);
    } catch (err) { 
        console.error("Message delivery failed:", err); 
    }
}

function updateDashboard(data) {
    if (!data) return;
    const metrics = data.metrics || data; 
    
    document.getElementById('energyVal').innerText = (metrics.energy || 0).toFixed(6) + ' kWh';
    document.getElementById('tokenVal').innerText = metrics.tokens || 0;
    document.getElementById('waterVal').innerText = (metrics.water || 0).toFixed(4) + 'L';
    
    const fillPercent = Math.min((metrics.water || 0) * 100, 100);
    document.getElementById('waterBar').style.height = fillPercent + '%';
}

function updateChart(logs) {
    const ctx = document.getElementById('historyChart').getContext('2d');
    const sortedForChart = [...logs].sort((a, b) => a.timestamp - b.timestamp);
    const waterData = sortedForChart.map(l => parseFloat(l.water) || 0);

    if (myChart) myChart.destroy();
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: waterData.map((_, i) => i + 1),
            datasets: [{
                data: waterData,
                borderColor: '#39ff14',
                borderWidth: 3,
                fill: true,
                backgroundColor: 'rgba(57, 255, 20, 0.1)',
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#39ff14'
            }]
        },
        options: { 
            maintainAspectRatio: false, 
            plugins: { legend: { display: false } }, 
            scales: { 
                y: { display: true, ticks: { color: '#39ff14', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.05)' } }, 
                x: { display: false } 
            } 
        }
    });
}

function updateGear(data) {
    const gear = document.getElementById('gearIndicator');
    const tokens = (data.metrics ? data.metrics.tokens : data.tokens) || 0;
    
    if (tokens < 800) {
        gear.innerText = "GRANITE 2B [ULTRA-ECO]";
        gear.className = "gear-low font-bold text-xl italic tracking-tighter";
    } else {
        gear.innerText = "GRANITE 8B [POWER-MODE]";
        gear.className = "gear-high font-bold text-xl italic tracking-tighter";
    }
}

async function loadTickets() {
    try {
        const resp = await fetch('http://127.0.0.1:8000/tickets');
        const tickets = await resp.json();
        document.getElementById('ticketList').innerHTML = tickets.map(t => `
            <div class="border-l-2 border-red-600 pl-2 bg-red-900/10 p-2 mb-2">
                <span class="neon-text-red font-bold">[RISK]:</span> ${t.title}
            </div>`).join('');
    } catch (err) { 
        console.warn("Could not retrieve tickets."); 
    }
}

async function resetSystem() {
    if (!confirm("Are you sure you want to reset the entire system?")) return;
    try {
        await fetch('http://127.0.0.1:8000/reset', { method: 'POST' });
        location.reload(); 
    } catch (err) { 
        alert("System reset failed!"); 
    }
}