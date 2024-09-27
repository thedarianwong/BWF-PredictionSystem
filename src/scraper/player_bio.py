import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_player_data(player_id):
    url = f"https://bwf.tournamentsoftware.com/player-profile/{player_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"Fetching data for player ID: {player_id}")
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = {'Player ID': player_id}
        
        # Name and Number (unchanged)
        media_content = soup.find('div', class_='media__content')
        if media_content:
            name_elem = media_content.select_one('span.nav-link__value')
            number_elem = media_content.select_one('span.media__title-aside')
            if name_elem:
                data['Name'] = name_elem.text.strip()
            if number_elem:
                data['Number'] = number_elem.text.strip('()')
        
        # Personal details (unchanged)
        module_container = soup.find('div', class_='module-container')
        if module_container:
            details = module_container.find_all('div', class_='list__item')
            for detail in details:
                label = detail.find('dt', class_='list__label')
                value = detail.find('dd', class_='list__value')
                if label and value:
                    key = label.text.strip()
                    val = value.text.strip()
                    if key == 'Height':
                        data['Height'] = val
                    elif key == 'Year of birth':
                        data['Year of Birth'] = val
                    elif key == 'Play R or L':
                        data['Play R or L'] = val
        
        # Win-Loss data
        win_loss_container = soup.find('div', id='tabStatsTotal')
        if win_loss_container:
            # Career (unchanged)
            career_item = win_loss_container.find('div', class_='list__item')
            if career_item:
                career_value = career_item.find('span', class_='list__value-start')
                if career_value:
                    data['Career'] = career_value.text.strip()
            
            # This year (updated)
            this_year_item = win_loss_container.find('dt', class_='list__label', string='This year')
            if this_year_item:
                this_year_value = this_year_item.find_next('span', class_='list__value-start')
                if this_year_value:
                    data['This Year'] = this_year_value.text.strip()
            
            # History (updated)
            history_list = win_loss_container.find('ul', class_='list--inline list')
            if history_list:
                print("Found history list")
                history_sequence = []
                for li in history_list.find_all('li', class_='list__item'):
                    span = li.find('span', class_='tag--round')
                    if span:
                        date = span.get('data-original-title', '').split(' ')[0]  # Extract date
                        result = 'W' if 'tag--success' in span.get('class', []) else 'L'
                        history_sequence.append(f"{date}: {result}")
                data['History'] = ' | '.join(history_sequence) if history_sequence else 'No history data found'
                print(f"History data: {data['History']}")
            else:
                print("History list not found")
                data['History'] = 'History list not found'
        else:
            print("Win-Loss container not found")
            data['History'] = 'Win-Loss container not found'

        print(f"Data found for player ID {player_id}: {data}")
        return data
    
    except requests.RequestException as e:
        print(f"Error fetching data for player ID {player_id}: {e}")
        return {'Player ID': player_id}

def main(player_ids, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Player ID', 'Name', 'Number', 'Height', 'Year of Birth', 'Play R or L', 'Career', 'This Year', 'History']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for player_id in player_ids:
            data = scrape_player_data(player_id)
            writer.writerow(data)
            time.sleep(2)  # Be respectful with request frequency

    print(f"Data collection complete. Results saved in {output_file}")

if __name__ == "__main__":
    player_ids = [
        "38CBD70E-A643-4170-9E6A-28863412DC7B",
        # Add more player IDs here
    ]
    main(player_ids, "bwf_player_data_extended.csv")