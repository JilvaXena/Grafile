from django.db import models

class ErrorCode(models.TextChoices):
    MISSING_FIELD = "MISSING_FIELD", "Missing fields in the request."
    GROUP_NOT_FOUND = "GROUP_NOT_FOUND", "Group ID provided is not in the system."
    FILE_NOT_FOUND = "FILE_NOT_FOUNT", "File ID provided is not in the system."
    INVALID_ALG = "INVALID_ALG", "Algorithm provided is not correct."
    MISSING_FILE_CONTENT = "MISSING_FILE_CONTENT", "File content was not found in the request."