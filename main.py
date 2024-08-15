import logging
import sys
from data_service.database.seed_arxiv import seed_arxiv_data
from data_service.services.scripts.chat_gpt import generate_podcast_script_for_paper
from data_service.services.audio_gen.aws_poly import generate_audio_for_paper

def main():
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) < 2:
        logging.error("Please provide a command (seed, generate, or audio).")
        return

    command = sys.argv[1]
    
    if command == 'seed':
        logging.info("Starting the arXiv database seeding process...")
        error = seed_arxiv_data()
        if error:
            logging.error(error)
        else:
            logging.info("Seeding process completed.")

    elif command == 'generate':
        if len(sys.argv) < 3:
            logging.error("Please provide a white paper ID to generate the script.")
            return

        paper_id = sys.argv[2]
        logging.info(f"Generating podcast script for paper ID: {paper_id}")
        script, error = generate_podcast_script_for_paper(paper_id)
        if error:
            logging.error(error)
        else:
            print("Generated Podcast Script:\n")
            print(script)

    elif command == 'audio':
        if len(sys.argv) < 3:
            logging.error("Please provide a white paper ID to generate the audio.")
            return

        paper_id = sys.argv[2]
        logging.info(f"Generating podcast audio for paper ID: {paper_id}")
        output_filename, error = generate_audio_for_paper(paper_id)
        if error:
            logging.error(error)
        else:
            logging.info(f"Audio file generated: {output_filename}")

    else:
        logging.error(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
