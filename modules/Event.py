"""Represents a single event."""
class Event:

    def __init__(self, name, time, org, img):
        """Construct an event object.

        Args:
            name (str): The name of the event
            time (list): The time of the event
            org (str): The organizer of the event
            img (str): The url of the event image

        Returns:
            Event: An event object.
        """
        self.name = name
        self.time = time
        self.org = org
        self.img = img

    def to_json(self):
        """Returns a JSON representation of the object.

        Returns: dict: A JSON representation of the object.
        """
        j = {}
        j['name'] = self.name
        j['time'] = self.time
        j['org'] = self.org
        j['img'] = self.img
        return j