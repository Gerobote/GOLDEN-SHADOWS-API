from fastapi import APIRouter, HTTPException
from typing import List
from app.db import db
from app.schemas import CaseCreate, CaseUpdate, CaseOut
from app.utils import to_object_id, serialize_doc

router = APIRouter()

@router.get("/", response_model=List[CaseOut])
async def list_cases():
    docs = await db().cases.find({}).to_list(length=1000)
    return [serialize_doc(d) for d in docs]

@router.get("/{case_id}", response_model=CaseOut)
async def get_case(case_id: str):
    try:
        _id = to_object_id(case_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid case id")
    doc = await db().cases.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="Case not found")
    return serialize_doc(doc)

@router.post("/", response_model=CaseOut, status_code=201)
async def create_case(payload: CaseCreate):
    result = await db().cases.insert_one(payload.model_dump())
    doc = await db().cases.find_one({"_id": result.inserted_id})
    return serialize_doc(doc)

@router.patch("/{case_id}", response_model=CaseOut)
async def update_case(case_id: str, patch: CaseUpdate):
    try:
        _id = to_object_id(case_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid case id")

    changes = {k: v for k, v in patch.model_dump(exclude_unset=True).items()}
    if not changes:
        raise HTTPException(status_code=400, detail="No fields to update")

    res = await db().cases.update_one({"_id": _id}, {"$set": changes})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Case not found")

    doc = await db().cases.find_one({"_id": _id})
    return serialize_doc(doc)

@router.delete("/{case_id}", status_code=204)
async def delete_case(case_id: str):
    try:
        _id = to_object_id(case_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid case id")

    res = await db().cases.delete_one({"_id": _id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Case not found")
    return None
