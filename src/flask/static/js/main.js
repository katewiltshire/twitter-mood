var $ = jQuery;

if (window.scores && $('#line-chart')) {

  var keys = Object.keys(window.scores.scores);

  new Chart($("#line-chart"), {
    type: 'line',
    data: {
      labels: keys,
      datasets: [{ 
          data: window.scores.data,
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
