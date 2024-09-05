console.log('settings.js is loading');

let topCoins = [];
let selectedCoins = JSON.parse(localStorage.getItem('selectedCoins')) || ['bitcoin', 'ethereum'];

function openSettingsModal() {
    console.log('openSettingsModal called');
    const settingsModal = document.getElementById('settingsModal');
    if (settingsModal) {
        settingsModal.style.display = 'block';
        fetchAndPopulateTopCoinList();
    } else {
        console.error('Settings modal not found');
    }
}

function closeSettingsModal() {
    console.log('Closing settings modal');
    const settingsModal = document.getElementById('settingsModal');
    if (settingsModal) {
        settingsModal.style.display = 'none';
    }
}

async function fetchAndPopulateTopCoinList() {
    try {
        if (topCoins.length === 0) {
            const response = await fetch('/get_top_coins');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            topCoins = await response.json();
        }
        populateCoinList(topCoins);
    } catch (error) {
        console.error('Error fetching top coins:', error);
        alert('Failed to fetch coin list. Please try again later.');
    }
}

function populateCoinList(coins) {
    const coinSelection = document.getElementById('coinSelection');
    coinSelection.innerHTML = '';
    coins.forEach(coin => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = coin.id;
        checkbox.checked = selectedCoins.includes(coin.id);

        const label = document.createElement('label');
        label.htmlFor = coin.id;
        label.textContent = `${coin.name} (${coin.symbol.toUpperCase()})`;

        const div = document.createElement('div');
        div.appendChild(checkbox);
        div.appendChild(label);

        coinSelection.appendChild(div);
    });
}

function saveSettings() {
    console.log('Saving settings');
    const newSelectedCoins = Array.from(document.querySelectorAll('#coinSelection input[type="checkbox"]:checked'))
        .map(checkbox => checkbox.id);
    
    console.log('New selected coins:', newSelectedCoins);
    
    if (JSON.stringify(newSelectedCoins) !== JSON.stringify(selectedCoins)) {
        selectedCoins = newSelectedCoins;
        localStorage.setItem('selectedCoins', JSON.stringify(selectedCoins));
        console.log('Saved selected coins:', selectedCoins);
        if (typeof window.updateSelectedCoins === 'function') {
            window.updateSelectedCoins(selectedCoins);
        } else {
            console.error('updateSelectedCoins function not found');
        }
        // Trigger an immediate update of the crypto data
        if (typeof refreshCryptoData === 'function') {
            refreshCryptoData();
        } else {
            console.error('refreshCryptoData function not found');
        }
    } else {
        console.log('No changes in selected coins');
    }
    
    closeSettingsModal();
}

// Make sure these functions are available globally
window.openSettingsModal = openSettingsModal;
window.closeSettingsModal = closeSettingsModal;
window.saveSettings = saveSettings;
