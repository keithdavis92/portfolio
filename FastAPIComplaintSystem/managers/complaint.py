import os
import uuid

from constants import TEMP_FILES_FOLDER
from db import database
from models import complaint, RoleType, State
from services.s3 import S3Service
from services.ses import SESService
from utils.helpers import decode_photo

s3 = S3Service()
ses = SESService()


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        # Get all complaints
        q = complaint.select()
        # If the role, is a complainer, filter q so they see their complaint only
        if user["role"] == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user["id"])
        # If the role is an approver, filter q so they only see pending complaints
        elif user["role"] == RoleType.approver:
            q = q.where(complaint.c.state == State.pending)
        # Otherwise the role will be admin and they can see all complaints
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data["complainer_id"] = user["id"]
        encoded_photo = complaint_data.pop("encoded_photo")
        extension = complaint_data.pop("extension")
        # Create random generated string along with the extension so that photo names are unique
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILES_FOLDER, name)
        decode_photo(path, encoded_photo)
        complaint_data["photo_url"] = s3.upload(path, name, extension)
        os.remove(path)
        # Create a complaint by inserting the new complaint data into the complaint database
        id_ = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=State.approved)
        )
        ses.send_mail("Complaint Approved", ["keithdavis92@gmail.com"], "Your claim has been approved, please allow "
                                                                        "for 3 days for your refund to process")

    @staticmethod
    async def reject(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=State.rejected)
        )
