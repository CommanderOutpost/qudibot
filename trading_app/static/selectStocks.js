const symbolInput = document.getElementById('symbolInput');
const symbolList = document.querySelector('.symbol-list');

symbolInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        addSymbol();
    }
});

function addSymbol() {
    const symbol = symbolInput.value.trim();
    if (symbol) {
        const symbolItem = document.createElement('span');
        symbolItem.classList.add('symbol-item');
        symbolItem.textContent = symbol.toUpperCase();

        const closeBtn = document.createElement('span');
        closeBtn.classList.add('close');
        closeBtn.textContent = '×';
        closeBtn.addEventListener('click', () => {
            symbolList.removeChild(symbolItem);
        });

        symbolItem.appendChild(closeBtn);
        symbolList.appendChild(symbolItem);
        symbolInput.value = '';
    }
}
