from pydantic import BaseModel

class HiredByQuarterResponse(BaseModel):
    department: str
    job: str
    q1: int
    q2: int
    q3: int
    q4: int

class DepartmentAboveMeanResponse(BaseModel):
    id: int
    department: str
    hired: int 