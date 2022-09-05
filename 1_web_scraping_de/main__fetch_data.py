import config as config

from helper__parse_job import DateExperience

import requests
from bs4 import BeautifulSoup

def read_experience_urls(sitemap_url: str) -> list:
    listing_urls = []
    try:
        sitemap_page = requests.get(sitemap_url)
        sitemap_xml = BeautifulSoup(sitemap_page.content, 'xml')
    except:
        print("Something went wrong while processing listing sitemap page.")
    else:
        listing_urls = [loc.text for loc in sitemap_xml.find_all("loc")]
        print(listing_urls[0:10])
    finally:
        return listing_urls

if __name__ == "__main__":
    # Read all Experience URLs from sitemap-listing
    experience_urls = read_experience_urls(config.URL__US_LISTING_SITEMAP)

    # Read each Experience, grabbing their data
    experiences = []
    for url in experience_urls:
        experience = DateExperience(url)
        if experience.valid_experience:
            experiences.append(experience)
    
