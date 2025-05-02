import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os
import time
import random

# Define user-agent to avoid bot blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_page_data(url, writer):
    print(f"Scraping page: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Correct selector for thread items
    thread_items = soup.select('.type-topic .bbp-topic-title')

    if not thread_items:
        print("No threads found, stopping scraper.")
        return None

    for item in thread_items:
        title_tag = item.find('a', class_='bbp-topic-permalink')
        if title_tag:
            title = title_tag.text.strip()
            thread_link = title_tag['href']
            print(f"Thread Title: {title}")
            writer.writerow([title, thread_link])

    # Find the next page link
    next_link = soup.find('a', class_='next page-numbers')
    if next_link:
        return urljoin(url, next_link['href'])

    return None

def scrape_all_pages(start_url, csv_filename):
    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Thread Title', 'Thread URL'])

        url = start_url
        while url:
            url = get_page_data(url, writer)
            time.sleep(random.uniform(1, 3))  # Be polite to the server

# Start scraping from the first page
start_url = 'https://wordpress.org/support/plugin/tutor/'
csv_filename = 'tutor_plugin_support_threads.csv'

scrape_all_pages(start_url, csv_filename)