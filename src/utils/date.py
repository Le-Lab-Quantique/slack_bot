from datetime import datetime

def format_date_string(date: str) -> str:
    """
    Formats a given date string into a human-readable format.
    Tries multiple formats before defaulting to an error message.
    """
    formats_to_try = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]
    for date_format in formats_to_try:
        try:
            parsed_date = datetime.strptime(date, date_format)
            return parsed_date.strftime("%A, %B %d, %Y at %I:%M %p")
        except ValueError:
            continue
    return "Invalid date format"