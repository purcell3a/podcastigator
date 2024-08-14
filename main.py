import logging
from data_service.database.seed_arxiv import seed_arxiv_data

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the arXiv database seeding process...")

    try:
        seed_arxiv_data()
        logging.info("Seeding process completed.")
    except Exception as e:
        logging.error(f"An error occurred during the seeding process: {e}")

if __name__ == "__main__":
    main()
