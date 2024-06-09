import time
import random
import requests
from bs4 import BeautifulSoup
import csv

def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def fetch_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html_content):
    return BeautifulSoup(html_content, 'html.parser')

def extract_data(soup):
    title = soup.title.string.strip() if soup.title else "No Title"
    h4_tags = soup.find_all('h4')
    h5_tags = soup.find_all('h5')
    groups = []

    for h4, h5 in zip(h4_tags, h5_tags):
        groups.append((h4.get_text(strip=True), h5.get_text(strip=True)))

    return title, groups

def save_data(data, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Group 1', 'Group 2', 'Group 3', 'Group 4'])
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    urls_file = 'Open_world_by_reviews.txt'
    urls = read_urls(urls_file)
    data = []

    for url in urls:
        html_content = fetch_page(url)
        if html_content:
            soup = parse_html(html_content)
            title, groups = extract_data(soup)
            row = [title] + [f"H4: {group[0]}, H5: {group[1]}" for group in groups]
            data.append(row)
        #add random delay between requests
        time.sleep(random.uniform(1, 5))


    save_data(data, 'output.csv')