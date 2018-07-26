var $ = jQuery;

if (window.scores && $('#line-chart')) {
  new Chart($("#line-chart"), {
    type: 'line',
    data: {
      labels: window.scores,
      datasets: [{ 
          data: window.scores,
          borderColor: "#3e95cd",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: false,
      }
    }
  });
}
