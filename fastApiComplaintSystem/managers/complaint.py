from db import database
from models import complaint, RoleType, State


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
        # Create a complaint by inserting the new complaint data into the complaint database
        id_ = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))
