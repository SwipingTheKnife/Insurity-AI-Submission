const gaugeContainer = document.getElementById('scoreGaugeContainer');
const avgScore = gaugeContainer.dataset.avgScore;       // string
const avgDiscount = gaugeContainer.dataset.avgDiscount; // string

const avgScoreNum = Number(avgScore);
const avgDiscountNum = Number(avgDiscount);

const ctx = document.getElementById('scoreGauge').getContext('2d');
const scoreGauge = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Score', 'Remaining'],
        datasets: [{
            data: [avgScoreNum, 100 - avgScoreNum],
            backgroundColor: ['rgba(75, 192, 192, 0.8)', 'rgba(235, 235, 235, 0.8)'],
            borderColor: 'white',
            borderWidth: 2,
            cutout: '80%',
            circumference: 180,
            rotation: 270,
            borderRadius: 5
        }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { enabled: false } } }
});

function updateScoreGauge(newValue) {
    scoreGauge.data.datasets[0].data[0] = newValue;
    scoreGauge.data.datasets[0].data[1] = 100 - newValue;
    scoreGauge.update({ duration: 800, easing: 'easeOutCubic' });
}

const maxDiscount = 20;

const ctx2 = document.getElementById('discountGauge').getContext('2d');
const discountGauge = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: ['Discount', 'Remaining'],
        datasets: [{
            data: [avgDiscountNum, maxDiscount - avgDiscountNum],
            backgroundColor: ['rgba(75, 192, 192, 0.8)', 'rgba(235, 235, 235, 0.8)'],
            borderColor: 'white',
            borderWidth: 2,
            cutout: '80%',
            circumference: 180,
            rotation: 270,
            borderRadius: 5
        }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { enabled: false } } }
});

function updateDiscountGauge(newValue) {
    discountGauge.data.datasets[0].data[0] = newValue;
    discountGauge.data.datasets[0].data[1] = maxDiscount - newValue;
    discountGauge.update({ duration: 800, easing: 'easeOutCubic'});
}

document.getElementById('scoreValue').textContent = `${avgScoreNum} / 100`;
document.getElementById('discountValue').textContent = `${avgDiscountNum}%`;

//Calculate Premium
const basePremium = 800;

const finalPremium = basePremium * (1 - avgDiscountNum / 100);

document.getElementById('premiumValue').textContent = `$${finalPremium.toFixed(2)}`;

//handles the json file, its the input for the Proof of Concept, in actual application the data would be uploaded constantly
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('jsonFile');
    if (!fileInput.files.length) return alert("Please select json file");

    const file = fileInput.files[0];
    const text = await file.text();
    let tripsJson;

    try {
        tripsJson = JSON.parse(text);
    } catch (error) {
        return alert("Invalid JSON file");
    }

    const response = await fetch('/upload_trips', {
        method: 'POST',
        headers: {'Content-Type': 'application/json' },
        body: JSON.stringify(tripsJson),
    });

    if (!response.ok) return alert('Failed to upload trips');

    const data = await response.json();

    document.getElementById('scoreValue').textContent = `${data.avg_driving_score.toFixed(2)}%`;
    document.getElementById('discountValue').textContent = `${data.avg_discount.toFixed(2)}%`;
    updateScoreGauge(data.avg_driving_score);
    updateDiscountGauge(data.avg_discount);

    const tripsContainer = document.querySelector('.RecentTrips');
    data.new_trips.forEach((trip, index) => {
    const p = document.createElement('p');
    p.textContent = `Trip: ${Math.round(trip.distance_miles)} miles, ${Math.round(trip.duration)} minutes, ${trip.weather}`;
    tripsContainer.appendChild(p);
});

    const newPremium = basePremium * (1 - data.avg_discount / 100);

    document.getElementById('premiumValue').textContent = `$${newPremium.toFixed(2)}`;


})