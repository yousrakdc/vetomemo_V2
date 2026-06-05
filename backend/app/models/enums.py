import enum


class Role(str, enum.Enum):
    owner = "owner"
    member = "member"
    vet_readonly = "vet_readonly"


class Species(str, enum.Enum):
    dog = "dog"
    cat = "cat"
    other = "other"


class HealthRecordType(str, enum.Enum):
    visit = "visit"
    vaccination = "vaccination"
    treatment = "treatment"