import os
import uuid

import dask.dataframe as dd
from celery import shared_task
from celery.result import AsyncResult
from fastapi.responses import FileResponse
from constants import TEMP_FILES_FOLDER


class SubmissionManager:
    @staticmethod
    def get_submission(submission_id):
        # Get the result from Redis backend
        ret_result = AsyncResult(submission_id)
        csv_name = f"{uuid.uuid4()}.csv"
        temp_file_path = os.path.join(TEMP_FILES_FOLDER, csv_name)
        ret_result.result.to_csv(temp_file_path, single_file=True)

        response = FileResponse(temp_file_path)
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"

        return response

    @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
                 name='submission:upload_submission')
    def upload_submission(self, in_file):
        # Create unique name for input csv
        csv_name = f"{uuid.uuid4()}.csv"
        temp_file_path = os.path.join(TEMP_FILES_FOLDER, csv_name)

        # Iteratively append to the temporary file with a max chunk size of 1MB to not use up memory
        with open(temp_file_path, 'ab') as temp_file:
            while content := in_file.file.read(1024):
                temp_file.write(content)

        in_file.file.close

        # Since we are required to output to a single file, we need to do some extra processing which may result in
        # some extended time. Files are by default written in parallel for Dask as single file output is a typical
        # bottleneck in big data processing.
        df = dd.read_csv(temp_file_path) \
            .rename(columns={"Number of Sales": "Total Sales for Date"}) \
            .groupby(['District', 'Date'])[['Total Sales for Date']].sum()

        return df
