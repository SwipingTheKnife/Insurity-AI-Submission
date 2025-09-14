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

    document.getElementById('discountValue').textContent = `${data.avg_discount.toFixed(2)}%`;

})