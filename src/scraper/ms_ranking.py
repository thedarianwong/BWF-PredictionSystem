import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime
import os

def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    print(f"Response status code for {url}: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")

    def extract_player_data(row):
        cells = row.find_all('td')
        if len(cells) >= 9:
            rank = cells[0].text.strip()
            player_name = cells[4].find('a').text.strip()
            player_link = cells[5].find('a')
            player_href = player_link['href'] if player_link else ''
            member_points = cells[7].text.strip()
            country = cells[10].text.strip()
            member_id = cells[6].text.strip()
            tournaments_played = cells[8].text.strip()

            return {
                'Rank': rank,
                'Name': player_name,
                'Member Points': member_points,
                'Country': country,
                'Member ID': member_id,
                'Tournaments Played': tournaments_played,
                'Profile Link': player_href
            }
        return None

    ruler_table = soup.find('table', class_='ruler')

    if ruler_table:
        print(f"Found table with class 'ruler' on {url}")
        rows = ruler_table.find_all('tr')
    else:
        print(f"Could not find table with class 'ruler' on {url}. Searching for alternative table structure...")
        rows = soup.find_all('tr')

    player_data = []

    for row in rows:
        player = extract_player_data(row)
        if player:
            player_data.append(player)

    if not player_data:
        print(f"\nNo player data found on {url}. Printing page structure for debugging:")
        print("\nAll tables found:")
        for i, table in enumerate(soup.find_all('table'), 1):
            print(f"Table {i} classes: {table.get('class', 'No class')}")
        
        print("\nAll div elements with 'id' attribute:")
        for div in soup.find_all('div', id=True):
            print(f"Div id: {div['id']}")
        
        print("\nFirst 1000 characters of the page content:")
        print(re.sub(r'\s+', ' ', soup.get_text())[:1000])

    return player_data

def save_to_csv(data, filename='ms_ranking.csv'):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    directory = os.path.join(project_root, 'data', 'raw')
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Rank', 'Name', 'Member ID', 'Country', 'Member Points', 'Tournaments Played', 'Profile Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for player in data:
            writer.writerow(player)

    return file_path

# URLs to scrape
urls = [
    "https://bwf.tournamentsoftware.com/ranking/category.aspx?rid=70&category=472&C472FOC=&p=1&ps=100",
    "https://bwf.tournamentsoftware.com/ranking/category.aspx?rid=70&category=472&C472FOC=&p=2&ps=100"
]

# Scrape all pages and combine results
all_player_data = []
for url in urls:
    all_player_data.extend(scrape_page(url))

# Save data to CSV file
if all_player_data:
    file_path = save_to_csv(all_player_data)
    print(f"\nData has been written to {file_path}")
    print(f"Total number of players scraped: {len(all_player_data)}")
else:
    print("\nNo player data found on any page. CSV file was not created.")

print("\nScript execution completed.")