console.log('Attempting to connect WebSocket...');
const socket = io();

let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

socket.on('connect', () => {
    console.log('WebSocket connected');
    reconnectAttempts = 0; // Reset the counter on successful connection
});

socket.on('connect_error', (error) => {
    console.error('WebSocket connection error:', error);
});

socket.on('update_prices', (data) => {
    console.log('Received price update:', data);
    if (typeof updateCryptoData === 'function') {
        updateCryptoData(data);
    } else {
        console.error('updateCryptoData function not found');
    }
});

socket.on('disconnect', () => {
    console.log('WebSocket disconnected. Attempting to reconnect...');
    reconnectWebSocket();
});

function reconnectWebSocket() {
    if (reconnectAttempts < maxReconnectAttempts) {
        setTimeout(() => {
            console.log(`Reconnection attempt ${reconnectAttempts + 1}`);
            socket.connect();
            reconnectAttempts++;
        }, 1000 * Math.pow(2, reconnectAttempts)); // Exponential backoff
    } else {
        console.error('Max reconnection attempts reached');
        if (typeof showNotification === 'function') {
            showNotification('Unable to connect to the server. Please refresh the page.', 'error');
        } else {
            console.error('showNotification function not found');
        }
    }
}
