# Cryptocurrency Dashboard

A real-time cryptocurrency tracking dashboard built with Flask and JavaScript.

## Features

- Real-time updates of cryptocurrency prices and market data
- User authentication system
- Customizable dashboard with selectable cryptocurrencies
- Dark mode toggle
- Responsive design for desktop and mobile devices
- WebSocket integration for live updates
- Error handling and user notifications
- Caching mechanism to handle API rate limits

## Technologies Used

- Backend: Flask, Flask-SocketIO, SQLAlchemy
- Frontend: HTML, CSS, JavaScript
- Real-time Communication: WebSockets (Socket.IO)
- API: CoinGecko for cryptocurrency data
- Database: SQLite (can be easily switched to other databases)
- Testing: Jest for JavaScript unit tests

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/crypto-dashboard.git
   cd crypto-dashboard
   ```

2. Set up a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URI=sqlite:///your_database.db
   ```

4. Initialize the database:
   ```
   flask db upgrade
   ```

5. Run the application:
   ```
   flask run
   ```

6. Open a web browser and navigate to `http://localhost:5000`

## Usage

- Register for an account or log in
- Use the settings modal to select your preferred cryptocurrencies
- Toggle dark mode using the switch in the header
- View real-time updates of cryptocurrency data on the dashboard

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [CoinGecko API](https://www.coingecko.com/en/api/documentation) for providing cryptocurrency data
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Socket.IO](https://socket.io/) for real-time communication
