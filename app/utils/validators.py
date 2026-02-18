from app.enums.application_status import ApplicationStatus
from app.core.exceptions import ConflictError


def validate_application_status_transition(
    current_status: ApplicationStatus,
    new_status: ApplicationStatus,
):
    allowed_transitions = {
        ApplicationStatus.APPLIED: [
            ApplicationStatus.SHORTLISTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WITHDRAWN,
        ],
        ApplicationStatus.SHORTLISTED: [
            ApplicationStatus.SELECTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WITHDRAWN,
        ],
        ApplicationStatus.REJECTED: [],
        ApplicationStatus.SELECTED: [],
        ApplicationStatus.WITHDRAWN: [],
    }

    if new_status not in allowed_transitions.get(current_status, []):
        raise ConflictError("Invalid status transition")
