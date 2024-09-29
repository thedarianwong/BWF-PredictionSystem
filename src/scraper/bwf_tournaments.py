import requests
from bs4 import BeautifulSoup
import csv
import os
import time

def scrape_bwf_tournaments(week_id, use_headers=True):
    url = f"https://bwf.tournamentsoftware.com/ranking/tournaments.aspx?id={week_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    } if use_headers else {}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', class_='ruler')
    if not table:
        print(f"No table found for week ID: {week_id}")
        return []

    rows = table.find_all('tr')

    data = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) == 5:
            number = cols[0].text.strip()
            
            tournament_link = cols[1].find('a')
            tournament_name = tournament_link.text.strip() if tournament_link else cols[1].text.strip()
            tournament_href = tournament_link['href'] if tournament_link else ''
            
            week = cols[2].text.strip()
            grading = cols[3].text.strip()
            processed_on = cols[4].text.strip()
            data.append([week_id, number, tournament_name, tournament_href, week, grading, processed_on])

    return data

def load_ranking_weeks(filename='ranking_weeks.csv'):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    file_path = os.path.join(project_root, 'data', 'raw', filename)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return [row[0] for row in reader]

def save_to_csv(data, filename='bwf_tournaments.csv', mode='a'):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    directory = os.path.join(project_root, 'data', 'raw')
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists or mode == 'w':
            writer.writerow(['Ranking Week ID', 'Number', 'Tournament', 'Tournament Link', 'Week', 'Grading', 'Processed on'])
        writer.writerows(data)

    return file_path

def main():
    week_ids = load_ranking_weeks()
    
    # Clear the existing file before starting
    save_to_csv([], mode='w')
    
    for week_id in week_ids:
        print(f"Scraping data for week ID: {week_id}")
        tournament_data = scrape_bwf_tournaments(week_id, use_headers=True)
        if tournament_data:
            saved_path = save_to_csv(tournament_data, mode='a')
            print(f"Data for week {week_id} appended to {saved_path}")
        else:
            print(f"No data found for week {week_id}")
        
        time.sleep(1)

    print("Scraping completed. All data saved to bwf_tournaments.csv")

if __name__ == "__main__":
    main()