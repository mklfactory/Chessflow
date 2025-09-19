# ♟️ ChessFlow - Console Tournament Manager

**ChessFlow** is a Python console application designed to manage chess tournaments smoothly, intuitively, and completely offline.

## 🔧 Features

- Creation and management of **players**
- Organization of **tournaments** with multiple **rounds**
- Automatic generation of **matches**
- Recording and updating of **scores**
- Performance tracking in a **history**
- Data saving and loading in **JSON** format
- Stylish console interface with **Rich**
- Interactive menu in **French**
- Option to **delete a round**
- Action logging for **debugging**

## 📂 Project Structure

Chessflow/
│
├── controllers/ # Application logic and controllers
├── models/ # Data models (players, tournaments, matches)
├── views/ # Console views & UI components
├── main.py # Application entry point
├── requirements.txt # Required dependencies
└── README.md # This file

## 🚀 Getting Started

1. Clone the repository:
git clone <https://github.com/mklfactory/Chessflow.git>
cd Chessflow

2. Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate # Windows
source .venv/bin/activate # macOS/Linux

3. Install dependencies:
pip install -r requirements.txt

4. Run the application from the project root:
python -m main


## 🎯 Usage

The application provides console menus to:

- Manage players and tournaments
- Enter and update match results
- View rankings and tournament progress
- Export and import data via JSON files

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📄 License

This project is licensed under the MIT License.