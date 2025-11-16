from zipfile import ZipFile
import os
import re

def unzip_file(file_name: str | None):

    if not file_name:
        return None

    with ZipFile(file_name, 'r') as zip_object:
        # List all files in the archive to identify desired members

        # Extract a specific file
        transcription = zip_object.extract('transcription.txt')
        # Extract another specific file to a different location
        info = zip_object.extract('info.txt')
        try:
            with open(transcription, 'r') as file:
                transcript = file.read()
                print(transcript)
            with open(info,'r') as file:
                text = file.read()

                # --- extract start time ---
                start_time_match = re.search(r"Start time:\s([^\n]+)", text)
                start_time = start_time_match.group(1).strip() if start_time_match else None

                # --- extract tracks ---
                # Gets everything after "Tracks:" until end of file or blank line
                tracks_block_match = re.search(r"Tracks:\s*(.*)", text, re.DOTALL)
                tracks_block = tracks_block_match.group(1).strip() if tracks_block_match else ""

                # Extract each track name (text before the first parenthesis)
                clean_list = [line.strip() for line in tracks_block.splitlines() if line.strip()]

                user_dict = {} 
                for pair in clean_list:
                    name, id = pair.split(" ")
                    user_dict[name] = id[1:-1]

                print("Start time:", start_time)
                print("Clean Dict:", user_dict, flush=True)

            return (transcript, start_time, user_dict)
        except FileNotFoundError:
            print(f"Error: The file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

