import threading
from Travel.models import Person, Book
from .logger import logger

class DatabaseThread(threading.Thread):
    def __init__(self, operation, **kwargs):
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs
        self.result = None
        self.error = None

    def run(self):
        try:
            logger.info(f"Starting {self.operation.__name__}")
            self.result = self.operation(**self.kwargs)
            logger.info(f"Completed {self.operation.__name__}")
        except Exception as e:
            self.error = e
            logger.error(f"Error in {self.operation.__name__}: {str(e)}")

def save_person_thread(**kwargs):
    logger.info(f"Saving person: {kwargs.get('username')}")
    person = Person(**kwargs)
    person.save()
    logger.info(f"Person saved: {kwargs.get('username')}")
    return person

def save_booking_thread(**kwargs):
    logger.info(f"Processing booking for: {kwargs.get('name')}")
    book = Book(**kwargs)
    book.save()
    logger.info(f"Booking completed for: {kwargs.get('name')}")
    return book

def perform_search(query):
    logger.info(f"Searching for: {query}")
    # Add your search logic here
    results = {"results": f"Found results for {query}"}
    logger.info(f"Search completed for: {query}")
    return results

def send_email_thread(**kwargs):
    logger.info(f"Sending email to: {kwargs.get('to_email')}")
    # Email sending logic here
    logger.info(f"Email sent to: {kwargs.get('to_email')}")
    pass

def export_data_thread(**kwargs):
    logger.info(f"Exporting data in {kwargs.get('format')} format")
    # Heavy data processing and export logic
    logger.info(f"Export completed for {kwargs.get('data_type')}")
    pass

# Example of how to use these threads in views:
def example_usage(user_email):
    """Example function showing how to use the threads"""
    # Send email example
    email_thread = DatabaseThread(
        send_email_thread,
        to_email=user_email,
        subject="Booking Confirmation"
    )
    email_thread.start()

    # Export data example
    export_thread = DatabaseThread(
        export_data_thread,
        format='csv',
        data_type='bookings'
    )
    export_thread.start() 