const submitBtn = document.getElementById('submitBtn');

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
            console.log(predictions)
            return predictions
        } else {
            throw new Error('Failed to get predictions');
        }

    } catch (error) {
        console.error(error);
    }
}

submitBtn.addEventListener('click', getPredictions);