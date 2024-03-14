const trades_array = []


function generateTradeCard(tradeData) {
  const cardHTML = `
      <div class="col-md-12">
        <div class="card mb-3 position-relative trade-card" card-trade-id="${tradeData.id}" data-trade-id="${tradeData.real_id}">
          <button type="button" class="btn-close position-absolute top-0 end-0 m-2" aria-label="Delete Trade" data-trade-id="${tradeData.id}"></button>
          <div class="card-body">
            <h5 class="card-title">Trade ${tradeData.id}</h5>
            <p class="card-text">
              <strong>Stock:</strong> ${tradeData.stock}<br>
              <strong>Strategy:</strong> ${tradeData.strategy}<br>
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
      real_id: trade.id,
      stock: trade.stock,
      strategy: trade.strategy,
      history: trade.history,
      range: `${trade.start_date} - ${trade.end_date}`,
      startTime: trade.time_started,
      endTime: trade.time_ended,
      profit: Math.floor(parseFloat(trade.profit) * 1000) / 1000,
      portfolioBalance: Math.floor(parseFloat(trade.portfolio_value) * 1000) / 1000
    };
    const cardHTML = generateTradeCard(tradeData);
    trades_array.push(tradeData)
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

  const deleteButtons = document.querySelectorAll('.btn-close');
  deleteButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
      const trade_id = e.target.getAttribute('data-trade-id');
      const trade_data = trades_array[trade_id - 1]
      const id = trade_data.real_id
      const confirmation = confirm('Are you sure you want to delete this trade?');
      if (!confirmation) {
        return;
      }
      const response = await fetch(`/delete_trade?trade_id=${id}`, { method: 'DELETE' });
      if (response.ok) {
        e.target.closest('.col-md-12').remove();
      }
    });
  });

  const tradeCards = document.querySelectorAll('.trade-card');
  tradeCards.forEach(card => {
    card.addEventListener('click', () => {
      const tradeId = card.getAttribute('card-trade-id');
      openTradeModal(tradeId);
    });
  });
}

function openTradeModal(tradeID) {
  const tradeHistory = trades_array[tradeID - 1].history;
  const modalContent = document.querySelector('.modal-body');
  modalContent.innerHTML = `
    <div>
      <h3>Trade History</h3>
      <ul>
        ${tradeHistory.map(trade => `
          <li>
            <strong>Operation:</strong> ${trade.operation}<br>
            <strong>Price:</strong> ${trade.price}<br>
            <strong>Amount:</strong> ${trade.amount}<br>
            <strong>Timestamp:</strong> ${trade.timestamp}<br>
            <strong>Insufficient Funds:</strong> ${trade.insufficent_funds}
          </li> <br>
        `).join('')}
      </ul>
    </div>
  `;

  // Show the modal
  const modal = bootstrap.Modal.getInstance(document.getElementById('tradeHistoryModal'));
  if (modal) {
    modal.show();
  } else {
    // Create a new instance if it doesn't exist
    const newModal = new bootstrap.Modal(document.getElementById('tradeHistoryModal'));
    newModal.show();
  }
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
