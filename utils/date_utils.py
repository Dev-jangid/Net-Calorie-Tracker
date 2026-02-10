from datetime import datetime, timedelta

def is_date_in_range(target_date: datetime.date, days_back: int = 30) -> bool:
    """
    Validates if a date is within the allowed range (last 30 days) and not in the future.
    """
    today = datetime.now().date()
    earliest_date = today - timedelta(days=days_back)
    
    if target_date > today:
        return False
    
    if target_date < earliest_date:
        return False
        
    return True

def format_date_for_db(dt: datetime.date) -> str:
    """
    Formats a date object to ISO string format YYYY-MM-DD.
    """
    return dt.strftime('%Y-%m-%d')
