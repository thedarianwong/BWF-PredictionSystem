# Badminton Tournament Prediction System

This project is a system for predicting outcomes in badminton tournaments using data scraped from the BWF website.

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd BWF-Prediction
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
   Note: Use `python` instead of `python3` if that's the command that works on your system.

3. Activate the virtual environment:
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Scraper

To run the web scraper and collect data:

```bash
python main.py
```

This will save the scraped data to `data/raw/world_rankings.json`.

## Project Structure

- `src/`: Contains the main source code
  - `scraper/`: Web scraping modules
  - `data/`: Data processing modules for ETL
- `tests/`: Unit tests
- `data/`: Stored data files
  - `raw/`: Raw scraped data
  - processed/ : Clean and transformed data
- `notebooks/`: Jupyter notebooks for data exploration
- `main.py`: Main script to run the scraper
