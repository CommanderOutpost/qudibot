const submitBtn = document.getElementById('submitBtn');
const predictionsContainer = document.querySelector('.prediction-container');


function getSymbols() {
    return Array.from(symbolList.children).map((symbol) => symbol.textContent.slice(0, -1));
}

async function getPredictions() {

    symbols = getSymbols();

    if (symbols.length === 0) {
        alert('Please select at least one stock');
        return;
    }

    try {
        const symbolList = document.querySelector('.symbol-list');
        const symbols = Array.from(symbolList.children).map((symbol) => symbol.textContent);

        const formData = new FormData();
        formData.append('stocks', symbols);

        const response = await fetch('/predictions', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            const predictions = data.predictions;
            renderPredictions(predictions);
            return predictions
        } else {
            throw new Error('Failed to get predictions');
        }

    } catch (error) {
        console.error(error);
    }
}

function renderPredictions(predictions) {
    console.log(predictions);
    console.log(typeof(predictions));

    if (!Array.isArray(predictions)) {
        console.error('Predictions is not an array:', predictions);
        return;
    }

    predictionsContainer.innerHTML = ''; // Clear previous predictions

    const row = document.createElement('div');
    row.classList.add('row');
    predictionsContainer.appendChild(row);

    predictions.forEach((prediction) => {
        const symbol = Object.keys(prediction)[0];
        const direction = prediction[symbol];

        const col = document.createElement('div');
        col.classList.add('col');

        const card = document.createElement('div');
        card.classList.add('card', direction === 'up' ? 'bg-success' : 'bg-danger', 'text-white');

        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        const title = document.createElement('h5');
        title.classList.add('card-title');
        title.textContent = symbol;

        const icon = document.createElement('i');
        icon.classList.add('fas', direction === 'up' ? 'fa-arrow-up' : 'fa-arrow-down', 'fa-2x');

        cardBody.appendChild(title);
        cardBody.appendChild(icon);
        card.appendChild(cardBody);
        col.appendChild(card);
        row.appendChild(col);
    });
}


function loadingSpinner(div) {
    const spinner = document.createElement('div');
    spinner.classList.add('spinner-border');
    spinner.setAttribute('role', 'status');
    spinner.innerHTML = '<span class="visually-hidden">Loading...</span>';
    div.appendChild(spinner);
    return spinner;
}

submitBtn.addEventListener('click', async () => {
    const spinner = loadingSpinner(predictionsContainer);
    await getPredictions();
});
