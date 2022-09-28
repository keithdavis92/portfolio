from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers.auth import oauth2_scheme, is_complainer, is_admin
from managers.complaint import ComplaintManager
from schemas.response.complaint import ComplaintOut
from schemas.request.complaint import ComplaintIn

router = APIRouter(tags=["Complaints"])


# Since we are returning all of the complaints, we are returning a list of ComplaintOuts
@router.get("/complaints/", dependencies=[Depends(oauth2_scheme)], response_model=List[ComplaintOut])
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplaintManager.get_complaints(user)


# Saves the user into the database and passes to authenication manager
# Authentication manager should return the login token
@router.post("/complaints/",
             dependencies=[Depends(oauth2_scheme),
                           Depends(is_complainer)],
             response_model=ComplaintOut)
async def create_complaint(request: Request, complaint: ComplaintIn):
    user = request.state.user
    return await ComplaintManager.create_complaint(complaint.dict(), user)


@router.delete("/complaints/{complaint_id}", dependencies=[Depends(oauth2_scheme), Depends(is_admin)], status_code=204)
async def delete_complaint(complaint_id: int):
    return await ComplaintManager.delete(complaint_id)
