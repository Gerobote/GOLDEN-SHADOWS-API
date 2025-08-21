from fastapi import APIRouter, HTTPException
from typing import List
from app.db import db
from app.schemas import DetectiveCreate, DetectiveUpdate, DetectiveOut
from app.utils import to_object_id, serialize_doc

router = APIRouter()

@router.get("/", response_model=List[DetectiveOut])
async def list_detectives():
    docs = await db().detectives.find({}).to_list(length=1000)
    return [serialize_doc(d) for d in docs]

@router.get("/{detective_id}", response_model=DetectiveOut)
async def get_detective(detective_id: str):
    try:
        _id = to_object_id(detective_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid detective id")
    doc = await db().detectives.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="Detective not found")
    return serialize_doc(doc)

@router.post("/", response_model=DetectiveOut, status_code=201)
async def create_detective(payload: DetectiveCreate):
    result = await db().detectives.insert_one(payload.model_dump())
    doc = await db().detectives.find_one({"_id": result.inserted_id})
    return serialize_doc(doc)

@router.patch("/{detective_id}", response_model=DetectiveOut)
async def update_detective(detective_id: str, patch: DetectiveUpdate):
    try:
        _id = to_object_id(detective_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid detective id")
    changes = {k: v for k, v in patch.model_dump(exclude_unset=True).items()}
    if not changes:
        raise HTTPException(status_code=400, detail="No fields to update")
    res = await db().detectives.update_one({"_id": _id}, {"$set": changes})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Detective not found")
    doc = await db().detectives.find_one({"_id": _id})
    return serialize_doc(doc)

@router.delete("/{detective_id}", status_code=204)
async def delete_detective(detective_id: str):
    try:
        _id = to_object_id(detective_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid detective id")
    res = await db().detectives.delete_one({"_id": _id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Detective not found")
    return None
