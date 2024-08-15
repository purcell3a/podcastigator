import boto3
import load_env
from pydub import AudioSegment
from data_service.services.scripts.chat_gpt import generate_podcast_script_for_paper
import os
from io import BytesIO

current_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables
AWS_ACCESS_KEY_ID = load_env.load_environment_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = load_env.load_environment_variable("AWS_SECRET_ACCESS_KEY")
AWS_REGION = load_env.load_environment_variable("AWS_REGION")

# Initialize Boto3 Polly client
polly_client = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
).client('polly')

def synthesize_speech(text, voice_id, output_filename):
    ssml_text = f"""
    <speak>
        {text}
    </speak>
    """

    try:
        response = polly_client.synthesize_speech(
            Text=ssml_text,
            OutputFormat="mp3",
            VoiceId=voice_id,
            TextType="ssml",  # Indicate that the input text is SSML
            Engine="neural"  # Use the neural engine
        )

        if "AudioStream" in response:
            return BytesIO(response['AudioStream'].read()), None  # Success, return in-memory stream
        else:
            return None, "No AudioStream found in the Polly response!"  # Error

    except Exception as e:
        return None, f"An error occurred during speech synthesis: {e}"

def generate_audio_for_paper(paper_id):
    # Define the intro file (make sure the path to the intro MP3 file is correct)
    INTRO_MP3 = os.path.join(current_dir, "INTRO_Ben_Fox_Deep_Blue_Synths_Percussion_Version.mp3")

    script, error = generate_podcast_script_for_paper(paper_id)
    if error:
        return None, error
    
    host_1_script = ""
    host_2_script = ""
    segments = []

    # Split the script by each line and determine which host is speaking
    for line in script.splitlines():
        if line.startswith("Host 1:"):
            host_1_script = line.replace("Host 1:", "").strip()
            if host_1_script:
                host_1_filename, error = synthesize_speech(host_1_script, "Matthew", f"host_1_{paper_id}_{len(segments)}.mp3")
                if error:
                    return None, error
                segments.append(host_1_filename)
        elif line.startswith("Host 2:"):
            host_2_script = line.replace("Host 2:", "").strip()
            if host_2_script:
                host_2_filename, error = synthesize_speech(host_2_script, "Joanna", f"host_2_{paper_id}_{len(segments)}.mp3")
                if error:
                    return None, error
                segments.append(host_2_filename)

    # Combine all audio segments into one file
    combined_audio = AudioSegment.empty()
    for segment_filename in segments:
        combined_audio += AudioSegment.from_mp3(segment_filename)
    
    # Export the combined host segments to a temporary file
    temp_output_filename = f"temp_podcast_{paper_id}.mp3"
    combined_audio.export(temp_output_filename, format="mp3")

    # Generate the final output filename by replacing "temp" with "final"
    final_output_file = f"final_podcast_{paper_id}.mp3"

    # Create the final output with the intro and voiceover combined
    create_intro_with_fade_and_voiceover(INTRO_MP3, temp_output_filename, final_output_file)

    return final_output_file, None

def create_intro_with_fade_and_voiceover(mp3_file, voiceover_file, output_file):
    # Load the MP3 intro file
    intro = AudioSegment.from_mp3(mp3_file)
    
    # Trim the intro to the first 3.5 seconds
    intro = intro[:3500]  # in milliseconds
    
    # Apply a fade-out starting at 3.5 seconds and ending at 5 seconds
    # Apply a fade-out effect (2 seconds)
    intro = intro.fade_out(duration=500)  # 1500 ms = 1.5 seconds fade duration
    
    # Load the voiceover file (the combined podcast audio)
    voiceover = AudioSegment.from_mp3(voiceover_file)
    
    # Create a silence segment for the first 3.5 seconds where the intro will play
    silence_before_voiceover = AudioSegment.silent(duration=1000)
    
    # Concatenate the silence + voiceover to the intro
    final_audio = intro + silence_before_voiceover + voiceover
    
    # Export the final mix as an MP3 file
    final_audio.export(output_file, format="mp3")
