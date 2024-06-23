import os

from dotenv import load_dotenv

from src.scrape_data import scrape
from src.format_data import generate_markdown

# Load .env file
load_dotenv()

client_id = os.getenv('CLIENT_ID')
bearer_token = os.getenv('BEARER_TOKEN')

def main():
    # First, scrape the data
    print("Scraping data from Truecoach...")
    scrape(client_id, bearer_token)

    # Then, format the data
    print("Formatting data as markdown...")
    generate_markdown()

    print("Done!")

if __name__ == "__main__":
    main()