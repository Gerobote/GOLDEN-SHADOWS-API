from fastapi import APIRouter, HTTPException
from typing import List
from app.db import db
from app.schemas import RelatedCaseCreate, RelatedCaseUpdate, RelatedCaseOut
from app.utils import to_object_id, serialize_doc

router = APIRouter()

@router.get("/", response_model=List[RelatedCaseOut])
async def list_related_cases():
    docs = await db().related_cases.find({}).to_list(length=1000)
    return [serialize_doc(d) for d in docs]

@router.get("/{rel_id}", response_model=RelatedCaseOut)
async def get_related_case(rel_id: str):
    try:
        _id = to_object_id(rel_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid id")
    doc = await db().related_cases.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="RelatedCase not found")
    return serialize_doc(doc)

@router.post("/", response_model=RelatedCaseOut, status_code=201)
async def create_related_case(payload: RelatedCaseCreate):
    result = await db().related_cases.insert_one(payload.model_dump())
    doc = await db().related_cases.find_one({"_id": result.inserted_id})
    return serialize_doc(doc)

@router.patch("/{rel_id}", response_model=RelatedCaseOut)
async def update_related_case(rel_id: str, patch: RelatedCaseUpdate):
    try:
        _id = to_object_id(rel_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid id")
    changes = {k: v for k, v in patch.model_dump(exclude_unset=True).items()}
    if not changes:
        raise HTTPException(status_code=400, detail="No fields to update")
    res = await db().related_cases.update_one({"_id": _id}, {"$set": changes})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="RelatedCase not found")
    doc = await db().related_cases.find_one({"_id": _id})
    return serialize_doc(doc)

@router.delete("/{rel_id}", status_code=204)
async def delete_related_case(rel_id: str):
    try:
        _id = to_object_id(rel_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid id")
    res = await db().related_cases.delete_one({"_id": _id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="RelatedCase not found")
    return None
