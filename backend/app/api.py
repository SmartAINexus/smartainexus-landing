import uuid

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import get_db
from app.models import Grant, NGO
from app.schemas import GrantCreate, GrantRead, NGOCreate, NGORead

router = APIRouter()


def tenant_id_header(
    x_tenant_id: uuid.UUID = Header(alias="X-Tenant-ID"),
    settings: Settings = Depends(get_settings),
) -> uuid.UUID:
    if settings.auth_mode != "development_header":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OIDC authentication is not configured",
        )
    return x_tenant_id


def require_tenant(db: Session, tenant_id: uuid.UUID) -> NGO:
    ngo = db.get(NGO, tenant_id)
    if ngo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return ngo


@router.post("/ngos", response_model=NGORead, status_code=status.HTTP_201_CREATED)
def register_ngo(payload: NGOCreate, db: Session = Depends(get_db)) -> NGO:
    ngo = NGO(**payload.model_dump())
    db.add(ngo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="NGO already registered")
    db.refresh(ngo)
    return ngo


@router.get("/ngos/me", response_model=NGORead)
def get_current_ngo(tenant_id: uuid.UUID = Depends(tenant_id_header),
                    db: Session = Depends(get_db)) -> NGO:
    return require_tenant(db, tenant_id)


@router.post("/grants", response_model=GrantRead, status_code=status.HTTP_201_CREATED)
def create_grant(payload: GrantCreate, tenant_id: uuid.UUID = Depends(tenant_id_header),
                 db: Session = Depends(get_db)) -> Grant:
    require_tenant(db, tenant_id)
    values = payload.model_dump()
    values["official_source_url"] = str(values["official_source_url"])
    grant = Grant(tenant_id=tenant_id, **values)
    db.add(grant)
    db.commit()
    db.refresh(grant)
    return grant


@router.get("/grants", response_model=list[GrantRead])
def list_grants(tenant_id: uuid.UUID = Depends(tenant_id_header),
                db: Session = Depends(get_db)) -> list[Grant]:
    require_tenant(db, tenant_id)
    return list(db.scalars(select(Grant).where(Grant.tenant_id == tenant_id).order_by(Grant.created_at)))


@router.get("/grants/{grant_id}", response_model=GrantRead)
def get_grant(grant_id: uuid.UUID, tenant_id: uuid.UUID = Depends(tenant_id_header),
              db: Session = Depends(get_db)) -> Grant:
    grant = db.scalar(select(Grant).where(Grant.id == grant_id, Grant.tenant_id == tenant_id))
    if grant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return grant
