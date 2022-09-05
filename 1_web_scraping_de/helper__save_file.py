import config as config
from helper__parse_job import DateExperience

def save_experiences_raw(experiences: list[DateExperience]) -> bool:
    try:
        for experience in experiences:
            print(experience.flat_features())
    except:
        print("Something went wrong while saving the Date Experiences to file.")

if __name__ == "__main__":
    print("hello")
