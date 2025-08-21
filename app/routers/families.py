from fastapi import APIRouter, HTTPException
from typing import List
from app.db import db
from app.schemas import FamilyCreate, FamilyUpdate, FamilyOut
from app.utils import to_object_id, serialize_doc

router = APIRouter()

@router.get("/", response_model=List[FamilyOut])
async def list_families():
    docs = await db().families.find({}).to_list(length=1000)
    return [serialize_doc(d) for d in docs]

@router.get("/{family_id}", response_model=FamilyOut)
async def get_family(family_id: str):
    try:
        _id = to_object_id(family_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid family id")
    doc = await db().families.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="Family not found")
    return serialize_doc(doc)

@router.post("/", response_model=FamilyOut, status_code=201)
async def create_family(payload: FamilyCreate):
    result = await db().families.insert_one(payload.model_dump())
    doc = await db().families.find_one({"_id": result.inserted_id})
    return serialize_doc(doc)

@router.patch("/{family_id}", response_model=FamilyOut)
async def update_family(family_id: str, patch: FamilyUpdate):
    try:
        _id = to_object_id(family_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid family id")
    changes = {k: v for k, v in patch.model_dump(exclude_unset=True).items()}
    if not changes:
        raise HTTPException(status_code=400, detail="No fields to update")
    res = await db().families.update_one({"_id": _id}, {"$set": changes})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Family not found")
    doc = await db().families.find_one({"_id": _id})
    return serialize_doc(doc)

@router.delete("/{family_id}", status_code=204)
async def delete_family(family_id: str):
    try:
        _id = to_object_id(family_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid family id")
    res = await db().families.delete_one({"_id": _id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Family not found")
    return None
