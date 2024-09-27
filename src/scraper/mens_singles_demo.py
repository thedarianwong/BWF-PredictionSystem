import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_bwf_rankings():
    url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?rid=70&category=472"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', class_='ruler')
            
            if table is None:
                print(f"Table not found. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                continue
            
            rows = table.find_all('tr')[2:]  # Skip the header rows
            
            data = []
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) > 0:
                    try:
                        rank = cols[0].text.strip() if len(cols) > 0 else ''
                        country_code = cols[3].text.strip() if len(cols) > 3 else ''
                        player = cols[4].find('a').text.strip() if len(cols) > 4 and cols[4].find('a') else ''
                        member_id = cols[5].text.strip() if len(cols) > 5 else ''
                        points = cols[6].text.strip() if len(cols) > 6 else ''
                        tournaments = cols[7].text.strip() if len(cols) > 7 else ''
                        confederation = cols[8].find('a').text.strip() if len(cols) > 8 and cols[8].find('a') else ''
                        country = cols[9].find('a').text.strip() if len(cols) > 9 and cols[9].find('a') else ''
                        
                        data.append({
                            'Rank': rank,
                            'Country Code': country_code,
                            'Player': player,
                            'Member ID': member_id,
                            'Points': points,
                            'Tournaments': tournaments,
                            'Confederation': confederation,
                            'Country': country
                        })
                    except IndexError as e:
                        print(f"Error processing row: {e}")
                        print(f"Row content: {row}")
                        continue
            
            if not data:
                print("No data was extracted. Printing table HTML for debugging:")
                print(table.prettify())
                return None
            
            return pd.DataFrame(data)
        
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Unable to scrape data.")
                return None

# Scrape the rankings
rankings_df = scrape_bwf_rankings()

if rankings_df is not None and not rankings_df.empty:
    # Display the first few rows
    print(rankings_df.head())

    # Save to CSV
    rankings_df.to_csv('bwf_mens_singles_rankings.csv', index=False)
else:
    print("Failed to scrape rankings data or no data was found.")