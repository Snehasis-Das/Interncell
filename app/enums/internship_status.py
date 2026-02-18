from enum import Enum


class InternshipStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class InternshipWorkMode(str, Enum):
    REMOTE = "remote"
    ONSITE = "onsite"
    HYBRID = "hybrid"


class InternshipTiming(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
