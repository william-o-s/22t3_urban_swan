import re
from bs4 import BeautifulSoup

def scrape_experience__alcohol():
    pass

def scrape_experience__category():
    pass

class DateExperience:
    def __init__(self, url: str, experience_html) -> None:
        """Stores a dictionary containing the Date Experience's details.
        @url: The Date Experience webpage URL.
        @experience_html: The rendered HTML content of the Experience webpage.
        """
        self.features = dict.fromkeys([
                                    'url',
                                    'experience_name',
                                    'duration',
                                    'day',
                                    'price_per_person__price',
                                    'price_per_person__currency',
                                    'location',
                                    'google_review__score',
                                    'google_review__num_reviews',
                                    'alcoholic',
                                    'category'
                                    ], None)
        self.features['url'] = url
        self.url = url
        self.experience_html = BeautifulSoup(experience_html, 'html.parser').find('body')

        # Verify Date Experience is valid
        assert self.fetch_experience()
        self.valid_experience = self.verify_experience()

        # Memory cleanup
        del self.url
        del self.experience_html

    def verify_experience(self) -> bool:
        """Checks if Date Experience is valid. Data fetch for Experience occurs
        as part of validation.
        
        Hierarchy of invalid values:
        1. URL ends with 13 digits, then 'x', then 18 digits
        2. Experience webpage does not contain:
            1. Name          
            2. Duration
            3. Day
            4. Location
        """

        # Invalid check 1
        if not self.url or re.search(r"\d{13}x\d{18}$", self.url):
            return False

        # Invalid check 2: requires GET on webpage
        if (not self.features['experience_name'] or
            not self.features['duration'] or
            not self.features['day'] or
            not self.features['location']):
            return False

        # All invalid checks passed
        return True
    
    def fetch_experience(self) -> bool:
        try:
            key_details_header = self.experience_html.find('div', class_="Text", string="Key details")
            self.key_details_container = key_details_header.parent.find_next_sibling('div', class_="column")
        except:
            print(f"Something went wrong while processing listing: {self.url}")
            return False
        else:
            self.scrape_experience__experience_name()  # NOTE: scrapes <meta> with exact properties
            self.scrape_experience__duration()  # NOTE: scrapes <div> with best guess
            self.scrape_experience__day()  # NOTE: scrapes <div> with best guess
            self.scrape_experience__price_per_person()  # NOTE: scrapes <meta> with exact properties
            self.scrape_experience__location()  # NOTE: scrapes <div> with best guess
            self.scrape_experience__google_review()  # NOTE: scrapes <div> with matching parentheses
            
            del self.key_details_container
            return True
        
    def scrape_experience__experience_name(self) -> bool:
        if not self.experience_html:
            return False
        
        try:
            experience_name = self.experience_html.find('meta', attrs={'property': "og:title"})
            self.features['experience_name'] = experience_name['content']
            return True
        except:
            print(f"Could not find Experience name for {self.url}.")
            return False

    def scrape_experience__duration(self) -> bool:
        if not self.experience_html:
            return False
        
        try:
            duration_container = self.key_details_container.find(
                                                                'div',
                                                                class_="row",
                                                                style=lambda style_attr: style_attr and
                                                                                        'z-index: 3' in style_attr)
            duration = duration_container.find('div', class_="Text")
            self.features['duration'] = duration.text.strip()
            return True
        except:
            print(f"Could not find duration for {self.url}.")
            return False

    def scrape_experience__day(self) -> bool:
        if not self.experience_html:
            return False
        
        try:
            day_container = self.key_details_container.find('div',
                                                            class_="row",
                                                            style=lambda style_attr: style_attr and
                                                                                    'z-index: 5' in style_attr)
            day = day_container.find('div', class_="Text")
            self.features['day'] = day.text.strip()
            return True
        except:
            print(f"Could not find available days for {self.url}.")
            return False

    def scrape_experience__price_per_person(self) -> bool:
        if not self.experience_html:
            return False

        try:
            price = self.experience_html.find('meta', attrs={'property': "og:price:amount"})
            currency = self.experience_html.find('meta', attrs={'property': "og:price:currency"})
            self.features['price_per_person__price'] = price['content']
            self.features['price_per_person__currency'] = currency['content']
            return True
        except:
            print(f"Could not find both price and currency for {self.url}.")
            return False

    def scrape_experience__location(self) -> bool:
        if not self.experience_html:
            return False
        
        try:
            location_container = self.key_details_container.find(
                                                                'div',
                                                                class_="row",
                                                                style=lambda style_attr: style_attr and
                                                                                        'z-index: 4' in style_attr)
            location = location_container.find('div', class_="Text")
            self.features['location'] = location.text.strip()
            return True
        except:
            print(f"Could not find location for {self.url}.")
            return False

    def scrape_experience__google_review(self) -> bool:
        if not self.experience_html:
            return False
        
        try:
            experience_header = self.experience_html.find('h1', id="experience-name").parent
            review_container = experience_header.find('button', class_="Icon").parent
            review_text = review_container.find('div',
                                                class_="Text",
                                                string=lambda text: '(' in text.lower()).text.strip()

            # Review text should be in format: "0.0 (000)"
            review_text = review_text.split()
            self.features['google_review__score'] = float(review_text[0])
            if review_text[1].startswith('(') and review_text[1].endswith(')'):
                self.features['google_review__num_reviews'] = int(review_text[1][1:-1])
            
            return True
        except:
            print(f"Could not find Google Reviews data for {self.url}.")
            self.features['google_review__score'] = None
            self.features['google_review__num_reviews'] = None
            return False
