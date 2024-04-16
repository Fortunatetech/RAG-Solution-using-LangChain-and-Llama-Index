import os
import shutil  
import textract 
import logging

def handle_uploads(upload_folder, data_folder, allowed_extensions):
    """
    Handles uploaded files.

    Args:
        upload_folder (str): Path to the temporary upload folder.
        data_folder (str): Path to the permanent data source folder.
        allowed_extensions (list): List of allowed file extensions (e.g., [".pdf", ".docx"])
    """

    for file_name in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, file_name)

        if not is_allowed_file(file_name, allowed_extensions):
            user_message = f"Invalid file type: {file_name}. Supported types: {allowed_extensions}"
            logging.error(user_message)
            continue

        if not is_valid_file(file_path):  
            user_message = f"File validation failed: {file_name}"
            logging.error(user_message) 
            # Display the 'user_message' to the frontend
            continue 

        try:
            text = process_and_extract_text(file_path)
        except Exception as e:
            user_message = f"Error processing file: {file_name}"
            logging.error(user_message, exc_info=True) 
            continue

        # Assuming your readers handle text and metadata separately
        metadata = {"source": "upload"} 
        document = {"text": text, "metadata": metadata}


        move_to_permanent_location(file_path, data_folder) 

# Helper functions
def is_allowed_file(file_name, allowed_extensions):
    _, extension = os.path.splitext(file_name)
    return extension.lower() in allowed_extensions

def is_valid_file(file_path, max_file_size_mb=10):
    """
    Performs basic file validation.
    """
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024) 

    if file_size_mb > max_file_size_mb:
        return False

    return True 

def process_and_extract_text(file_path):
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()  

    if extension in [".pdf", ".docx"]:
        text = textract.process(file_path).decode()
    elif extension == ".txt":
        with open(file_path, "r") as f:
            text = f.read()
    else:
        # Handle other file types or log an unsupported file error
        return None  

    return text  

def move_to_permanent_location(file_path, data_folder):
    shutil.move(file_path, data_folder)
