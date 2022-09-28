from datetime import datetime

from models import State
from schemas.base import BaseComplaint


# Inherit schema from BaseComplaint class
class ComplaintOut(BaseComplaint):
    id: int
    created_at: datetime
    status: State
