import zipfile
import os

def extract_zip(file_path, extract_path):
    """
    Extracts the individual files from a zip file at the given path
    to the specified extract path and returns a list of extracted file paths.

    Args:
        file_path (str): The path to the zip file.
        extract_path (str): The path to extract files to.

    Returns:
        list: A list of file paths of the extracted files.
    """
    extracted_files = []
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        for file_info in zip_ref.infolist():
            extracted_file_path = zip_ref.extract(file_info, path=extract_path)
            absolute_file_path = os.path.abspath(extracted_file_path)
            extracted_files.append(absolute_file_path)
    return extracted_files


def sanitize_url(url:str) -> str:
    new_url = url.split("/")[-1].split(".")[0]
    return new_url.replace(" ", "_").lower()


def truncate_string(input_string, max_length=63):
    if len(input_string) > max_length:
        return input_string[:max_length]
    else:
        return input_string
