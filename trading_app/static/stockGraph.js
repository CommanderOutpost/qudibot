function createStockGraph(data, stock) {
    const dateTimeList = data.Date;
    // Convert the datetime of type datetime to the correct format string yyyy-mm-dd
    for (let i = 0; i < dateTimeList.length; i++) {
        const date = new Date(dateTimeList[i]);
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const formattedTime = `${year}-${month}-${day}`;
        dateTimeList[i] = formattedTime;
    }

    console.log(dateTimeList)
    

    const trace = {
        x: data.Date,
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

    console.log(trace)

    const layout = {
        title: `${stock} Live Share Price`,
        xaxis: {
            type: 'date',
            title: 'Date',
            range: [data.Date[0], data.Date[data.Date.length - 1]],
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
    const interval = '1d';

    console.log(stock, period, interval)

    const response = await fetch(`/get_stock_data?stock=${stock}&period=${period}&interval=${interval}`);
    const data = await response.json();

    console.log(data)

    createStockGraph(data, stock);

});
