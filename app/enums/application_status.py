from enum import Enum


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    SELECTED = "selected"
    WITHDRAWN = "withdrawn"
