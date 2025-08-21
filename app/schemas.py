from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

# ---------- Victim ----------
class VictimCreate(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0)
    family_id: Optional[str] = None
    murder_method_id: Optional[str] = None
    case_ids: List[str] = []

class VictimUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0)
    family_id: Optional[str] = None
    murder_method_id: Optional[str] = None
    case_ids: Optional[List[str]] = None

class VictimOut(BaseModel):
    id: str
    name: str
    age: int
    family_id: Optional[str] = None
    murder_method_id: Optional[str] = None
    case_ids: List[str] = []

# ---------- Case ----------
class CaseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    opened_at: datetime = Field(default_factory=datetime.utcnow)
    detective_ids: List[str] = []
    victim_ids: List[str] = []
    related_case_ids: List[str] = []

class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    opened_at: Optional[datetime] = None
    detective_ids: Optional[List[str]] = None
    victim_ids: Optional[List[str]] = None
    related_case_ids: Optional[List[str]] = None

class CaseOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    opened_at: datetime
    detective_ids: List[str] = []
    victim_ids: List[str] = []
    related_case_ids: List[str] = []

# ---------- Family ----------
class FamilyCreate(BaseModel):
    name: str = Field(..., min_length=1)
    motto: Optional[str] = None

class FamilyUpdate(BaseModel):
    name: Optional[str] = None
    motto: Optional[str] = None

class FamilyOut(BaseModel):
    id: str
    name: str
    motto: Optional[str] = None

# ---------- MurderMethod ----------
class MurderMethodCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None

class MurderMethodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class MurderMethodOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

# ---------- Detective ----------
class DetectiveCreate(BaseModel):
    name: str = Field(..., min_length=1)
    rank: Optional[str] = None
    rumored_to_be_killer: bool = False
    studies: Optional[str] = None

class DetectiveUpdate(BaseModel):
    name: Optional[str] = None
    rank: Optional[str] = None
    rumored_to_be_killer: Optional[bool] = None
    studies: Optional[str] = None

class DetectiveOut(BaseModel):
    id: str
    name: str
    rank: Optional[str] = None
    rumored_to_be_killer: bool
    studies: Optional[str] = None

# ---------- RelatedCase ----------
class RelatedCaseCreate(BaseModel):
    case_id: str
    related_to_case_id: str
    relation: Optional[str] = None  # e.g., "same MO", "timeline overlap"

class RelatedCaseUpdate(BaseModel):
    case_id: Optional[str] = None
    related_to_case_id: Optional[str] = None
    relation: Optional[str] = None

class RelatedCaseOut(BaseModel):
    id: str
    case_id: str
    related_to_case_id: str
    relation: Optional[str] = None

# ---------- MediaReport (opcional) ----------
class MediaReportCreate(BaseModel):
    case_id: str
    title: str
    url: Optional[str] = None
    published_at: datetime = Field(default_factory=datetime.utcnow)

class MediaReportUpdate(BaseModel):
    case_id: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    published_at: Optional[datetime] = None

class MediaReportOut(BaseModel):
    id: str
    case_id: str
    title: str
    url: Optional[str] = None
    published_at: datetime
