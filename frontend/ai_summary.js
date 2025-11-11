const API_URL = 'http://127.0.0.1:8000';
const token = localStorage.getItem('access_token');

const summaryText = document.getElementById('summary-text');
const suggestionsList = document.getElementById('suggestions-list');
const resourceLinks = document.getElementById('resource-links');
const backBtn = document.getElementById('back-btn');
const chartCanvas = document.getElementById('progressChart');

let chartInstance = null;

if (!token) {
  window.location.href = 'index.html';
}

backBtn.addEventListener('click', () => {
  window.location.href = 'dashboard.html';
});

async function fetchSummary() {
  summaryText.textContent = 'Generating your AI summary...';

  try {
    const response = await fetch(`${API_URL}/progress/summary`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    const data = await response.json();

    if (!response.ok) {
      summaryText.textContent = '⚠️ Error fetching AI summary.';
      console.error(data);
      return;
    }
    summaryText.textContent = data.summary || "No AI summary available.";
    suggestionsList.innerHTML = '';
    if (data.suggestions && data.suggestions.length > 0) {
      data.suggestions.forEach(s => {
        const li = document.createElement('li');
        li.textContent = s;
        suggestionsList.appendChild(li);
      });
    } else {
      suggestionsList.innerHTML = '<li>No suggestions available.</li>';
    }
    if (data.progress_distribution && Object.keys(data.progress_distribution).length > 0) {
      renderChart(data.progress_distribution);
    } else {
      renderChart({
        "Python": 40,
        "Math": 30,
        "DSA": 30
      });
    }
    const subjects = Object.keys(data.progress_distribution || {});
    generateResourceLinks(subjects);

  } catch (err) {
    summaryText.textContent = '⚠️ Could not connect to the AI service.';
    console.error('Fetch error:', err);
  }
}

function renderChart(distribution) {
  if (!chartCanvas) return;

  const ctx = chartCanvas.getContext('2d');
  const labels = Object.keys(distribution);
  const values = Object.values(distribution);

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: 'pie',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: ['#8BC34A', '#FFC107', '#03A9F4', '#E91E63', '#9C27B0'],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#3D4127', font: { size: 14 } }
        },
        title: {
          display: true,
          text: "Study Time Distribution by Subject",
          font: { size: 18, weight: 'bold' }
        }
      }
    }
  });
}

function generateResourceLinks(subjects) {
  resourceLinks.innerHTML = '';
  if (!subjects || subjects.length === 0) {
    resourceLinks.innerHTML = '<li>No topics found to recommend.</li>';
    return;
  }

  subjects.forEach(sub => {
    const li = document.createElement('li');
    li.innerHTML = `
      <a href="https://www.youtube.com/results?search_query=${encodeURIComponent(sub + ' tutorial for beginners')}"
         target="_blank">
        🎥 ${sub} — Watch recommended tutorials
      </a>`;
    resourceLinks.appendChild(li);
  });
}

fetchSummary();
