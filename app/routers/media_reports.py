from fastapi import APIRouter, HTTPException
from typing import List
from app.db import db
from app.schemas import MediaReportCreate, MediaReportUpdate, MediaReportOut
from app.utils import to_object_id, serialize_doc

router = APIRouter()

@router.get("/", response_model=List[MediaReportOut])
async def list_media_reports():
    docs = await db().media_reports.find({}).to_list(length=1000)
    return [serialize_doc(d) for d in docs]

@router.get("/{report_id}", response_model=MediaReportOut)
async def get_media_report(report_id: str):
    try:
        _id = to_object_id(report_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid report id")
    doc = await db().media_reports.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="MediaReport not found")
    return serialize_doc(doc)

@router.post("/", response_model=MediaReportOut, status_code=201)
async def create_media_report(payload: MediaReportCreate):
    result = await db().media_reports.insert_one(payload.model_dump())
    doc = await db().media_reports.find_one({"_id": result.inserted_id})
    return serialize_doc(doc)

@router.patch("/{report_id}", response_model=MediaReportOut)
async def update_media_report(report_id: str, patch: MediaReportUpdate):
    try:
        _id = to_object_id(report_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid report id")
    changes = {k: v for k, v in patch.model_dump(exclude_unset=True).items()}
    if not changes:
        raise HTTPException(status_code=400, detail="No fields to update")
    res = await db().media_reports.update_one({"_id": _id}, {"$set": changes})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="MediaReport not found")
    doc = await db().media_reports.find_one({"_id": _id})
    return serialize_doc(doc)

@router.delete("/{report_id}", status_code=204)
async def delete_media_report(report_id: str):
    try:
        _id = to_object_id(report_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid report id")
    res = await db().media_reports.delete_one({"_id": _id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="MediaReport not found")
    return None
