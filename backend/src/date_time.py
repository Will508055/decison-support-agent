from datetime import datetime

# Get current date and time at device location and format for LLM prompt
def get_date_time() -> str:
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%H:%M on %B %d, %Y')
    return formatted_datetime