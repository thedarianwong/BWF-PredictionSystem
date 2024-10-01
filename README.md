# Badminton Tournament Prediction System

This project is a system for predicting outcomes in badminton tournaments using data scraped from the BWF website.

## Prerequisites
1. Download Docker - https://docs.docker.com/desktop/install/mac-install/
2. Download Docker-Compose
## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd BWF-Prediction
   ```

2. Build the Docker images:
   ```bash
   ./docker-manage.sh build
   ```

3. Start the Docker images:
   ```bash
   ./docker-manage.sh start
   ```

4. Stop the Docker images:
   ```bash
   ./docker-manage.sh stop
   ```
   
5. For Docker help:
  ```bash
   ./docker-manage.sh help
   ```

6. Running the scraper for Development purposes:
   ```bash
   ./docker-manage.sh exec python <script name>.py
   ```

## Project Structure

- `src/`: Contains the main source code
  - `scraper/`: Web scraping modules
  - `data/`: Data processing modules for ETL
- `aws/`: Scripts to configure and modify files using AWS
- `data/`: Stored data files
  - `raw/`: Raw scraped data
  - `processed/`: Clean and transformed data
- `docker/`: Docker-related files
  - `Dockerfile`: Main Dockerfile for the application
- `docker-compose.yml`: Docker Compose configuration
- `docker-manage.sh`: Script to manage Docker operations

## Owner's Comment

This project is still in the early phase, our goal is to create a project to understand more about data engineering and data visualization. At the same time, we are badminton enthusiasts that regularly follows the BWF tournaments throughout the year, so we thought it would be cool to have a prediction model to see who will win the future upcoming tournamments.
