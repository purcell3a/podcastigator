import logging
import sys
from data_service.database.seed_arxiv import seed_arxiv_data
from data_service.services.scripts.chat_gpt import generate_podcast_script_for_paper

def main():
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "seed":
            logging.info("Starting the arXiv database seeding process...")
            try:
                seed_arxiv_data()
                logging.info("Seeding process completed.")
            except Exception as e:
                logging.error(f"An error occurred during the seeding process: {e}")

        elif command == "generate":
            if len(sys.argv) < 3:
                logging.error("Please provide a paper ID to generate the podcast script.")
                return

            paper_id = sys.argv[2]
            logging.info(f"Generating podcast script for paper ID: {paper_id}")
            generate_podcast_script_for_paper(paper_id)

        else:
            logging.error(f"Unknown command: {command}")
            print("Available commands: seed, generate <paper_id>")

    else:
        logging.error("No command provided. Use 'seed' to seed the database or 'generate <paper_id>' to generate a podcast script.")

if __name__ == "__main__":
    main()