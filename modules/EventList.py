"""Contains all events of a given day."""
class EventList:

    errors = [] # Contains errors that occur during scrape

    def __init__(self, day, events):
        """Construct an event list object.

        Args:
            day (str): The calendar date of the events
            events (list): A list of events

        Returns:
            EventList: An event list object.
        """
        self.day = day
        self.events = events

    def to_json(self):
        """Returns a JSON representation of the object.

        Returns: dict: A JSON representation of the object.
        """
        j = {}
        j['day'] = self.day
        j['events'] = [e.to_json() for e in self.events]
        j['errors'] = self.errors
        return j