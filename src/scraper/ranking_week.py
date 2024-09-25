import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_ranking_week_ids(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    select_tag = soup.find('select', {'name': 'ctl00$ctl00$ctl00$cphPage$cphPage$cphPage$dlPublication'})
    if not select_tag:
        print("Select tag not found. The page structure might have changed.")
        return []

    week_ids = []
    for option in select_tag.find_all('option'):
        week_id = option['value']
        week_text = option.text.strip()
        week_ids.append((week_id, week_text))

    return week_ids
def save_to_csv(data, filename='ranking_weeks.csv'):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    directory = os.path.join(project_root, 'data', 'raw')
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Week ID', 'Week Text'])
        writer.writerows(data)

    return file_path

if __name__ == "__main__":
    url = "https://bwf.tournamentsoftware.com/ranking/tournaments.aspx?id=42400"
    week_ids = scrape_ranking_week_ids(url)
    if week_ids:
        saved_path = save_to_csv(week_ids)
        print(f"Ranking week IDs saved to {saved_path}")
    else:
        print("No ranking week IDs found.")