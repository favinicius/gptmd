from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func

from src.database.config import get_session
from src.database.models import HardwareTable, LaborRoleTable, ActivityTable, LogisticsItemTable, SettingsTable

router = APIRouter(prefix="/registers", tags=["Registers"])

# --- Hardware Routes ---
@router.get("/hardware", response_model=List[HardwareTable])
def read_hardware(
    offset: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(HardwareTable)
    if search:
        query = query.where(
            (HardwareTable.description_base.contains(search)) | 
            (HardwareTable.partnumber.contains(search))
        )
    if category:
        query = query.where(HardwareTable.category == category)
        
    query = query.offset(offset).limit(limit)
    return session.exec(query).all()

@router.post("/hardware", response_model=HardwareTable)
def create_hardware(item: HardwareTable, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.put("/hardware/{item_id}", response_model=HardwareTable)
def update_hardware(item_id: int, item_update: HardwareTable, session: Session = Depends(get_session)):
    db_item = session.get(HardwareTable, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Hardware item not found")
    
    item_data = item_update.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
        
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.delete("/hardware/{item_id}")
def delete_hardware(item_id: int, session: Session = Depends(get_session)):
    db_item = session.get(HardwareTable, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Hardware item not found")
    session.delete(db_item)
    session.commit()
    return {"ok": True}

# --- Labor Routes ---
@router.get("/labor/roles", response_model=List[LaborRoleTable])
def read_roles(session: Session = Depends(get_session)):
    return session.exec(select(LaborRoleTable)).all()

@router.get("/labor/activities", response_model=List[ActivityTable])
def read_activities(
    offset: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(ActivityTable)
    if search:
         query = query.where(ActivityTable.name.contains(search) | ActivityTable.description.contains(search))
    query = query.offset(offset).limit(limit)
    return session.exec(query).all()

@router.post("/labor/activities", response_model=ActivityTable)
def create_activity(item: ActivityTable, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

# --- Logistics/Settings Routes ---
@router.get("/logistics", response_model=List[LogisticsItemTable])
def read_logistics(session: Session = Depends(get_session)):
    return session.exec(select(LogisticsItemTable)).all()

@router.get("/settings", response_model=List[SettingsTable])
def read_settings(session: Session = Depends(get_session)):
    return session.exec(select(SettingsTable)).all()
