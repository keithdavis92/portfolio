from typing import Optional, List

from fastapi import APIRouter, Depends

from managers.auth import is_admin, oauth2_scheme, is_approver
from managers.complaint import ComplaintManager
from managers.user import UserManager
from models import RoleType
from schemas.response.user import UserOut

router = APIRouter(tags=["Users"])


@router.get(
    "/users/",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    response_model=List[UserOut],
)
async def get_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()


@router.put(
    "/users/{user_id}/make-admin",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_admin(user_id: int):
    return await UserManager.change_role(RoleType.admin, user_id)


@router.put(
    "/users/{user_id}/make-approver",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_approver(user_id: int):
    return await UserManager.change_role(RoleType.approver, user_id)


@router.put(
    "/complaints/{complaint_id}/approve",
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
    status_code=204,
)
async def approve(complaint_id: int):
    return await ComplaintManager.approve(complaint_id)


@router.put(
    "/complaints/{complaint_id}/reject",
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
    status_code=204,
)
async def reject(complaint_id: int):
    return await ComplaintManager.reject(complaint_id)
