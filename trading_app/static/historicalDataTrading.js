function generateTradeCard(tradeData) {
    const cardHTML = `
      <div class="col-md-12">
        <div class="card mb-3 position-relative">
          <button type="button" class="btn-close position-absolute top-0 end-0 m-2" aria-label="Delete Trade" data-trade-id="${tradeData.id}"></button>
          <div class="card-body">
            <h5 class="card-title">Trade ${tradeData.id}</h5>
            <p class="card-text">
              <strong>Stock:</strong> ${tradeData.stock}<br>
              <strong>Range:</strong> ${tradeData.range}<br>
              <strong>Start Time:</strong> ${tradeData.startTime}<br>
              <strong>End Time:</strong> ${tradeData.endTime}<br>
              <strong>Profit:</strong> $${tradeData.profit}<br>
              <strong>Portfolio Balance:</strong> $${tradeData.portfolioBalance}
            </p>
          </div>
        </div>
      </div>
    `;
    return cardHTML;
}

function renderTrades(trades) {
    console.log(trades)
    const cardsContainer = document.getElementById('trade-cards-container');
    if (trades.length === 0) {
        cardsContainer.classList.add('text-center');
        cardsContainer.innerHTML = '<h3>No trade history available</h3>';
        return;
    }

    cardsContainer.classList.remove('text-center');
    trades.forEach((trade, index) => {
        const tradeData = {
            id: index + 1,
            stock: trade.stock,
            range: `${trade.start_date} - ${trade.end_date}`,
            startTime: trade.time_started,
            endTime: trade.time_ended,
            profit: trade.profit,
            portfolioBalance: trade.portfolio_value
        };
        const cardHTML = generateTradeCard(tradeData);
        cardsContainer.insertAdjacentHTML('beforeend', cardHTML);
    });
    // Add a button to clear the trade history
    const clearButton = `
      <div class="col-md-12">
        <button id="clear-trades" class="btn btn-danger btn-lg">Clear Trade History</button>
      </div>
    `;
    cardsContainer.insertAdjacentHTML('beforeend', clearButton);

    // Add an event listener to the clear trade history button
    const clearTradesButton = document.getElementById('clear-trades');
    clearTradesButton.addEventListener('click', async () => {
        // Alert the user before clearing the trade history
        const confirmation = confirm('Are you sure you want to clear your trade history?');
        if (!confirmation) {
            return;
        }
        const response = await fetch('/clear_trades', { method: 'DELETE' });
        if (response.ok) {
            cardsContainer.innerHTML = '';
        }
    });
}

async function fetchTrades() {
    try {
        const response = await fetch('/get_trades');
        if (response.ok) {
            const trades = await response.json()
            renderTrades(trades)
            return trades
        }
        throw new Error("Error fetching trades")
    } catch (error) {
        console.log(error)
    }
}

fetchTrades()
