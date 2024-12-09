import re

def format_job_details(job_details):
    """Cleans and formats job details to remove any extra characters, HTML tags, or unwanted data."""
    formatted_details = {}
    for key, value in job_details.items():
        if isinstance(value, str):
            # Remove newlines, tabs, and multiple spaces
            cleaned_value = re.sub(r'\s+', ' ', value).strip()
            # Remove any JSON-like content if accidentally captured
            if cleaned_value.startswith('{') and cleaned_value.endswith('}'):
                cleaned_value = 'Not available'
            formatted_details[key] = cleaned_value
        else:
            formatted_details[key] = value

    return formatted_details
