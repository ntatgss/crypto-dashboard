console.log('crypto_updates.js is loading');

const socket = io({
    auth: {
        token: document.querySelector('meta[name="user_id"]').getAttribute('content')
    }
});

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('update_crypto_data', (response) => {
    console.log('Received real-time update:', response);
    if (response && response.data) {
        updateCryptoData(response.data, response.is_stale);
    } else {
        console.error('Received invalid data structure:', response);
    }
});

function updateCryptoData(data, isStale) {
    console.log('Updating crypto data:', data, 'Stale:', isStale);
    const cryptoGrid = document.querySelector('.crypto-grid');
    if (!cryptoGrid) {
        console.error('Crypto grid not found in the DOM');
        return;
    }

    // Clear existing cards
    cryptoGrid.innerHTML = '';

    // Update or remove the stale data indicator
    let staleIndicator = document.getElementById('stale-data-indicator');
    if (isStale) {
        if (!staleIndicator) {
            staleIndicator = document.createElement('div');
            staleIndicator.id = 'stale-data-indicator';
            staleIndicator.textContent = 'Using cached data';
            staleIndicator.style.backgroundColor = 'yellow';
            staleIndicator.style.padding = '10px';
            staleIndicator.style.textAlign = 'center';
            document.body.insertBefore(staleIndicator, cryptoGrid);
        }
    } else if (staleIndicator) {
        staleIndicator.remove();
    }

    if (Array.isArray(data)) {
        data.forEach(coin => {
            console.log(`Creating/updating card for ${coin.id}:`, {
                name: coin.name,
                symbol: coin.symbol,
                current_price: coin.current_price,
                price_change_percentage_24h: coin.price_change_percentage_24h,
                market_cap: coin.market_cap,
                total_volume: coin.total_volume
            });
            const card = createCryptoCard(coin);
            cryptoGrid.appendChild(card);
        });
        console.log(`Updated ${data.length} crypto cards`);
    } else {
        console.error('Received data is not an array:', data);
    }
}

function createCryptoCard(coin) {
    const card = document.createElement('div');
    card.className = 'crypto-card';
    card.id = `card-${coin.id}`;
    
    // Add null checks for each property
    const name = coin.name || 'Unknown';
    const symbol = coin.symbol ? coin.symbol.toUpperCase() : 'N/A';
    const currentPrice = formatNumber(coin.current_price);
    const priceChange = coin.price_change_percentage_24h ? coin.price_change_percentage_24h.toFixed(2) : 'N/A';
    const marketCap = formatNumber(coin.market_cap);
    const volume = formatNumber(coin.total_volume);  // Changed from coin.volume to coin.total_volume

    card.innerHTML = `
        <h2>${name} (${symbol})</h2>
        <p>Price: $<span class="price">${currentPrice}</span></p>
        <p>24h Change: <span class="change">${priceChange}%</span></p>
        <p>Market Cap: $<span class="market-cap">${marketCap}</span></p>
        <p>24h Volume: $<span class="volume">${volume}</span></p>
    `;
    
    updateCryptoCard(card, coin);
    return card;
}

function updateCryptoCard(card, coin) {
    const priceElement = card.querySelector('.price');
    const changeElement = card.querySelector('.change');
    const marketCapElement = card.querySelector('.market-cap');
    const volumeElement = card.querySelector('.volume');

    if (priceElement && changeElement && marketCapElement && volumeElement) {
        const oldPrice = parseFloat(priceElement.textContent.replace('$', '').replace(',', ''));
        const newPrice = coin.current_price;
        console.log(`Updating ${coin.id}: Old price: ${oldPrice}, New price: ${newPrice}`);

        const priceChangeClass = (coin.price_change_percentage_24h >= 0) ? 'positive' : 'negative';
        const priceChangeAnimation = (newPrice > oldPrice) ? 'price-up' : (newPrice < oldPrice ? 'price-down' : '');
        
        priceElement.textContent = formatNumber(newPrice);
        priceElement.className = `price ${priceChangeAnimation}`;
        changeElement.textContent = `${formatNumber(coin.price_change_percentage_24h)}%`;
        changeElement.className = `change ${priceChangeClass}`;
        marketCapElement.textContent = formatNumber(coin.market_cap);
        volumeElement.textContent = formatNumber(coin.total_volume);  // Changed from coin.volume to coin.total_volume
        
        setTimeout(() => {
            priceElement.classList.remove('price-up', 'price-down');
        }, 1000);
    } else {
        console.error(`One or more elements not found in the card for ${coin.id}`);
    }
}

function formatNumber(num) {
    if (num === undefined || num === null) {
        return 'N/A';
    }
    
    if (typeof num !== 'number') {
        console.warn(`Expected a number, but got ${typeof num}: ${num}`);
        return 'N/A';
    }

    if (num >= 1e9) {
        return (num / 1e9).toFixed(2) + 'B';
    } else if (num >= 1e6) {
        return (num / 1e6).toFixed(2) + 'M';
    } else if (num >= 1e3) {
        return (num / 1e3).toFixed(2) + 'K';
    } else {
        return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
}

window.updateSelectedCoins = function(selectedCoins) {
    console.log('Updating selected coins:', selectedCoins);
    localStorage.setItem('selectedCoins', JSON.stringify(selectedCoins));
    socket.emit('update_selected_coins', selectedCoins);
};

// Initial load of crypto data
document.addEventListener('DOMContentLoaded', function() {
    const selectedCoins = JSON.parse(localStorage.getItem('selectedCoins')) || ['bitcoin', 'ethereum'];
    window.updateSelectedCoins(selectedCoins);
    refreshCryptoData(); // Add this line to load data when the page loads
});

function refreshCryptoData() {
    console.log('Refreshing crypto data');
    const selectedCoins = JSON.parse(localStorage.getItem('selectedCoins')) || ['bitcoin', 'ethereum'];
    console.log('Selected coins for refresh:', selectedCoins);
    
    // Fetch new data from the server
    fetch(`/get_crypto_data?coins=${selectedCoins.join(',')}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received new crypto data:', data);
            if (data.error) {
                throw new Error(data.error);
            }
            updateCryptoData(data, false);
        })
        .catch(error => {
            console.error('Error fetching crypto data:', error);
            showErrorMessage('Failed to fetch crypto data. Please try again later.');
        });
}

function showErrorMessage(message) {
    const cryptoGrid = document.querySelector('.crypto-grid');
    if (cryptoGrid) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        cryptoGrid.innerHTML = '';
        cryptoGrid.appendChild(errorDiv);
    }
}

// Make sure this function is available globally
window.refreshCryptoData = refreshCryptoData;
