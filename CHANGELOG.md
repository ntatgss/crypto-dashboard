# Cryptocurrency Dashboard Changelog

## [Unreleased]

## [0.5.0] - 2023-09-05
### Added
- Implemented fallback data functionality
- Added get_all_coins endpoint for fetching available cryptocurrencies
- Implemented error boundaries in JavaScript functions
- Added proper WebSocket error handling and reconnection logic
- Included comments for complex code sections

### Changed
- Resolved discrepancy between availableCoins and allCoins in settings.js
- Removed duplicate socket initialization from crypto_updates.js
- Updated requirements.txt with exact dependency versions

### Fixed
- Improved error handling in both frontend and backend

## [0.4.0] - 2023-09-05
### Changed
- Moved "Cryptocurrency Dashboard" heading to the main body and increased its size
- Repositioned settings button and dark mode toggle in the header
- Improved overall layout and responsiveness of the dashboard
- Refactored CSS for better organization and maintainability

### Fixed
- Resolved issues with button positioning in the header
- Fixed duplicate "Cryptocurrency Dashboard" heading

## [0.3.0] - 2023-09-04
### Added
- User customization feature allowing selection of displayed cryptocurrencies
- Settings modal for cryptocurrency selection
- Persistent user preferences using local storage
- Fallback dataset for when API calls fail
- More detailed console logging for debugging

### Changed
- Increased number of displayed cryptocurrencies from 10 to 20
- Improved dark mode to include settings modal
- Enhanced API rate limit handling with more aggressive caching and backoff strategy
- Reduced frequency of API calls to respect rate limits

### Fixed
- Readability issues in dark mode for settings modal

## [0.2.0] - 2023-09-04
### Added
- Dark mode toggle with persistent user preference
- Visual feedback for price changes (color coding and animations)
- Simulated price movements between API calls

### Changed
- Improved responsive design for various screen sizes
- Enhanced error handling for API requests

## [0.1.0] - 2023-09-04
### Added
- Initial release of the Cryptocurrency Dashboard
- Flask backend with Flask-SocketIO for real-time updates
- Frontend with responsive grid layout for cryptocurrency data
- Integration with CoinGecko API for fetching cryptocurrency data
- Basic caching mechanism to handle API rate limits
- Real-time price and market cap updates using WebSocket
- Display of top 10 cryptocurrencies by market cap

[Unreleased]: https://github.com/yourusername/crypto-dashboard/compare/v0.4.0...HEAD
[0.5.0]: https://github.com/yourusername/crypto-dashboard/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/yourusername/crypto-dashboard/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/yourusername/crypto-dashboard/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/yourusername/crypto-dashboard/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/yourusername/crypto-dashboard/releases/tag/v0.1.0
