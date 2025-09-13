// Get the canvas context
const ctx = document.getElementById('scoreGauge').getContext('2d');

// Chart data and options
const data = {
  labels: ['Value', 'Remaining'], // Customize labels as needed
  datasets: [{
    data: [75, 25], // Example: 75% filled, 25% remaining
    backgroundColor: ['rgba(75, 192, 192, 0.8)', 'rgba(235, 235, 235, 0.8)'],
    borderColor: 'white',
    borderWidth: 2,
    cutout: '80%', // Adjust for desired thickness
    circumference: 180, // Half-circle
    rotation: 270, // Start from the bottom-left
    borderRadius: 5,
  }],
};

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false, // Hide legend
    },
    tooltip: {
      enabled: false, // Hide tooltips
    },
  },
};

// Create the chart
const scoreGauge = new Chart(ctx, {
  type: 'doughnut',
  data: data,
  options: options,
});



// Get the canvas context
const ctx2 = document.getElementById('discountGauge').getContext('2d');

// Chart data and options
const data2 = {
  labels: ['Value', 'Remaining'], // Customize labels as needed
  datasets: [{
    data: [75, 25], // Example: 75% filled, 25% remaining
    backgroundColor: ['rgba(75, 192, 192, 0.8)', 'rgba(235, 235, 235, 0.8)'],
    borderColor: 'white',
    borderWidth: 2,
    cutout: '80%', // Adjust for desired thickness
    circumference: 180, // Half-circle
    rotation: 270, // Start from the bottom-left
    borderRadius: 5,
  }],
};

const options2 = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false, // Hide legend
    },
    tooltip: {
      enabled: false, // Hide tooltips
    },
  },
};

// Create the chart
const discountGauge = new Chart(ctx2, {
  type: 'doughnut',
  data: data2,
  options: options2,
});