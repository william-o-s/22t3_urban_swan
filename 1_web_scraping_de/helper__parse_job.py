import re
import requests
from bs4 import BeautifulSoup

class DateExperience:
    def __init__(self, url: str) -> None:
        """Create a DateExperience object containing default Experience values.
        @url: The Date Experience webpage URL.
        """
        self.url = url
        self.initialize_experience()
        # Verify Date Experience is valid - data fetch guaranteed
        self.valid_experience = self.verify_experience()

    def initialize_experience(self) -> None:
        self.features = {
            'url': self.url,
            'experience_name': None,
            'duration': None,
            'day': None,
            'price_per_person': {
                'type': 'fixed',
                'price': 0,
                'discounted_price': 0
            },
            'location': {
                'type': 'single',
                'locations': []
            },
            'google_review': {
                'score': 0,
                'num_reviews': 0
            },
            'alcoholic': False,
            'dnd_vouchers': False,
            'category': None
        }
    
    def flat_features(self) -> dict:
        return {
            'url': self.features['url'],
            'experience_name': self.features['experience_name'],
            'duration': self.features['duration'],
            'day': self.features['day'],
            'price_per_person__type': self.features['price_per_person']['type'],
            'price_per_person__price': self.features['price_per_person']['price'],
            'price_per_person__discounted_price': self.features['price_per_person']['discounted_price'],
            'location__type': self.features['location']['type'],
            'location__locations': self.features['location']['locations'],
            'google_review__score': self.features['google_review']['score'],
            'google_review__num_reviews': self.features['google_review']['num_reviews'],
            'alcoholic': self.features['alcoholic'],
            'dnd_vouchers': self.features['dnd_vouchers'],
            'category': self.features['category']
        }

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
        assert self.fetch_experience()
        if (not self.features['experience_name'] or
            not self.features['duration'] or
            not self.features['day'] or
            not self.features['location']['locations']):
            return False

        # All invalid checks passed
        return True
    
    def fetch_experience(self) -> bool:
        success = True
        try:
            experience_page = requests.get(self.url)
            experience_html = BeautifulSoup(experience_page.content, 'html.parser')
        except:
            print(f"Something went wrong while processing listing: ${self.url}")
            success = False
        else:
            pass
        finally:
            return success

if __name__ == "__main__":
    print("hello")
