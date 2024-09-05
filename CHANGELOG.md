# Cryptocurrency Dashboard Changelog

## [Unreleased]

## [0.6.0] - 2023-09-06
### Added
- Implemented user authentication system with login and registration functionality
- Added user-specific coin selection and persistence
- Integrated Flask-Login for user session management
- Created new routes for login, logout, and registration
- Implemented rate limiting decorator for API endpoints
- Added SocketIO events for real-time updates of selected coins
- Created a background task for periodic data updates
- Implemented a global TOP_COINS list with periodic updates
- Added new components: header and settings modal
- Created a Config class for centralized configuration management
- Implemented user settings management (get_user_coins, update_user_coins)
- Added Flask extensions management (SQLAlchemy, Migrate, LoginManager, SocketIO)

### Changed
- Refactored routes to use Blueprint
- Updated the dashboard to show user-specific selected coins
- Improved error handling in both frontend and backend
- Enhanced the settings modal to use the global TOP_COINS list
- Updated the header component to include login/logout links
- Moved database and SocketIO initialization to extensions.py

### Fixed
- Resolved issues with user authentication and coin selection persistence
- Improved error handling for API requests and WebSocket connections

### Security
- Implemented proper password hashing for user accounts
- Added login required decorators to protect routes

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
