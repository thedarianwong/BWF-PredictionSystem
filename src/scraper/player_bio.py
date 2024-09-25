import requests
from bs4 import BeautifulSoup

def scrape_player_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the main content div
    content_div = soup.find('div', class_='module__content')
    
    # Personal details
    personal_details = {}
    details_div = content_div.find('div', class_='module-container')
    if details_div:
        details = details_div.find_all('div', class_='margin-bottom')
        for detail in details:
            label = detail.find('div', class_='text-muted').text.strip()
            value = detail.find('div', class_='text-right').text.strip()
            personal_details[label] = value
    
    # Win-Loss data
    win_loss = {}
    win_loss_div = content_div.find('div', class_='js-tabs-container')
    if win_loss_div:
        categories = win_loss_div.find_all('div', class_='margin-bottom')
        for category in categories:
            label = category.find('div', class_='text-muted').text.strip()
            value = category.find('div', class_='text-right').text.strip()
            win_loss[label] = value
    
    return {
        'personal_details': personal_details,
        'win_loss': win_loss
    }

# Usage
url = "https://bwf.tournamentsoftware.com/player/[PLAYER_ID]"  # Replace [PLAYER_ID] with actual ID
player_data = scrape_player_details(url)

print("Personal Details:")
for key, value in player_data['personal_details'].items():
    print(f"{key}: {value}")

print("\nWin-Loss Data:")
for key, value in player_data['win_loss'].items():
    print(f"{key}: {value}")