function createStockGraph(data) {
    const trace = {
        x: data.Datetime,
        open: data.Open,
        high: data.High,
        low: data.Low,
        close: data.Close,
        type: 'candlestick',
        xaxis: 'x',
        yaxis: 'y',
        increasing: { line: { color: '#17BECF' } },
        decreasing: { line: { color: '#7F7F7F' } }
    };

    const layout = {
        title: `${stock} Live Share Price`,
        xaxis: {
            type: 'date',
            title: 'Date',
            range: [data.Datetime[0], data.Datetime[data.Datetime.length - 1]],
            rangeselector: {
                buttons: [
                    { count: 1, label: '1D', step: 'day', stepmode: 'backward' },
                    { count: 7, label: '1W', step: 'day', stepmode: 'backward' },
                    { count: 1, label: '1M', step: 'month', stepmode: 'backward' },
                    { step: 'all' }
                ]
            },
            rangeslider: { visible: true }
        },
        yaxis: { title: 'Stock Price (USD per Shares)' }
    };

    Plotly.newPlot('stock-graph', [trace], layout);
}

const stockForm = document.getElementById('stock-form');
stockForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const stock = document.getElementById('stock').value;
    const period = document.getElementById('period').value;
    const interval = document.getElementById('interval').value;

    const response = await fetch(`/get_stock_data?stock=${stock}&period=${period}&interval=${interval}`);
    const data = await response.json();

    createStockGraph(data);

});
