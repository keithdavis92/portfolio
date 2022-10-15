from schemas.base import BaseComplaint


# Inherit schema from BaseComplaint class
class ComplaintIn(BaseComplaint):
    encoded_photo: str
    extension: str

