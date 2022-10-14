from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse

from managers.submission import SubmissionManager

router = APIRouter(tags=["Submission"])


@router.get("/submission/{submission_id}")
async def get_submission(submission_id: str):
    return SubmissionManager.get_submission(submission_id)


# Obtain the posted data and process it
@router.post("/submission/")
async def upload_submission(file: UploadFile = File(...)):
    submission = SubmissionManager.upload_submission.delay(file)
    return JSONResponse({"task_id": submission.id})
