document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('assetAllocationChart');
    if (!ctx) return; // Don't run if the chart element isn't on the page
  
    // Retrieve data from the data attributes
    const labels = JSON.parse(ctx.dataset.labels);
    const values = JSON.parse(ctx.dataset.values);
  
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: 'Asset Allocation',
          data: values,
          backgroundColor: [
            'rgb(54, 162, 235)', // Blue
            'rgb(255, 205, 86)', // Yellow
            'rgb(255, 99, 132)'  // Red
          ],
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: false,
            text: 'Asset Allocation'
          }
        }
      }
    });
  });