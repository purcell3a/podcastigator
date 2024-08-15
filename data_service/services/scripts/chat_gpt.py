import openai
import load_env
from data_service.database.db_connection import fetch_paper_metadata

OPENAI_API_KEY = load_env.load_environment_variable("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def generate_conversational_script_with_gpt(paper_metadata):
    title = paper_metadata["title"]
    abstract = paper_metadata["abstract"]
    authors = ', '.join(paper_metadata["authors"])  # Convert list to comma-separated string
    primary_category = paper_metadata["primary_category"]

    prompt = f"""
    I have the following research paper details, and I need a podcast script that includes a conversation between two hosts:

    Title: {title}
    Abstract: {abstract}
    Authors: {authors}
    Primary Category: {primary_category}

    Please generate a conversational podcast script where two hosts discuss this paper.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or whichever model you're using
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates conversational podcast scripts."},
            {"role": "user", "content": prompt}
        ]
    )

    script = response['choices'][0]['message']['content'].strip()
    return script


def generate_podcast_script_for_paper(paper_id):
    # Fetch the paper metadata from the database
    paper_metadata = fetch_paper_metadata(paper_id)
    
    if paper_metadata:
        # Generate the conversational script using OpenAI API
        script = generate_conversational_script_with_gpt(paper_metadata)
        print(script)
        return script, None  # Return the script and no error
    else:
        return None, f"No paper found with ID: {paper_id}"  # Return None and an error message
