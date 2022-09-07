import config as config

from helper__parse_job import DateExperience

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

def read_experience_urls(sitemap_url: str) -> list:
    listing_urls = []
    try:
        sitemap_page = requests.get(sitemap_url)
        sitemap_xml = BeautifulSoup(sitemap_page.content, 'xml')
    except:
        print("Something went wrong while processing listing sitemap page.")
    else:
        listing_urls = [loc.text for loc in sitemap_xml.find_all("loc")]
    finally:
        return listing_urls

def save_experiences_xlsx(valid_experiences: list, invalid_experiences: list) -> bool:
    try:
        valid_experiences_df = pd.DataFrame.from_records(valid_experiences)
        invalid_experiences_df = pd.DataFrame.from_records(invalid_experiences)
        
        print("Attempting to save Experiences to file.")
        with pd.ExcelWriter(path=config.FILE__EXPERIENCES_DATA, engine='openpyxl', mode='w') as writer:
            if not valid_experiences_df.empty:
                valid_experiences_df.to_excel(
                                            excel_writer=writer,
                                            sheet_name=config.SHEET_VALID_EXPERIENCES,
                                            float_format="%.2f",
                                            index=False)
            if not invalid_experiences_df.empty:
                invalid_experiences_df.to_excel(
                                            excel_writer=writer,
                                            sheet_name=config.SHEET_INVALID_EXPERIENCES,
                                            float_format="%.2f",
                                            index=False)
        return True
    except Exception as err:
        print(err)
        print("Something went wrong while saving the Date Experiences to file.")
        return False

if __name__ == "__main__":
    # Read all Experience URLs from sitemap-listing
    experience_urls = read_experience_urls(config.URL__US_LISTING_SITEMAP)
    total_experiences = len(experience_urls)
    print(f"Processing {total_experiences} Experiences. Loading...")

    # Read each Experience, grabbing their data
    session = HTMLSession()
    valid_experiences = []
    invalid_experiences = []
    counter = 1
    for url in experience_urls:
        request = session.get(url)
        request.html.render(timeout=15, sleep=15)
        experience = DateExperience(url, request.html.html)
        if experience.valid_experience:
            valid_experiences.append(experience.features)
        else:
            invalid_experiences.append(experience.features)
        print(f"Processed {counter}/{total_experiences} Experiences.")
        counter += 1
    
    print(f"Total valid experiences: {len(valid_experiences)}")
    print(f"Total invalid experiences: {len(invalid_experiences)}")
    assert save_experiences_xlsx(valid_experiences, invalid_experiences)
