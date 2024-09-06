// static/js/crypto_updates.test.js

import '@testing-library/jest-dom';
import { render, screen, fireEvent } from '@testing-library/react';
import { refreshCryptoData, updateCryptoData } from './crypto_updates';

// Mock fetch function
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve([{ id: 'bitcoin', name: 'Bitcoin', current_price: 50000 }]),
  })
);

describe('Crypto Updates', () => {
  test('refreshCryptoData fetches and updates data', async () => {
    // Setup
    document.body.innerHTML = '<div class="crypto-grid"></div>';
    localStorage.setItem('selectedCoins', JSON.stringify(['bitcoin']));

    // Execute
    await refreshCryptoData();

    // Assert
    expect(fetch).toHaveBeenCalledWith('/get_crypto_data?coins=bitcoin');
    expect(document.querySelector('.crypto-grid')).toHaveTextContent('Bitcoin');
    expect(document.querySelector('.crypto-grid')).toHaveTextContent('$50,000');
  });

  test('updateCryptoData creates crypto cards', () => {
    // Setup
    document.body.innerHTML = '<div class="crypto-grid"></div>';
    const data = [{ id: 'ethereum', name: 'Ethereum', current_price: 3000 }];

    // Execute
    updateCryptoData(data, false);

    // Assert
    expect(document.querySelector('.crypto-grid')).toHaveTextContent('Ethereum');
    expect(document.querySelector('.crypto-grid')).toHaveTextContent('$3,000');
  });
});