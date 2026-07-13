import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, field_validator


class NGOCreate(BaseModel):
    official_name: str = Field(min_length=2, max_length=200)
    registration_number: str = Field(min_length=2, max_length=80, pattern=r"^[A-Za-z0-9./_-]+$")
    country_code: str = Field(min_length=2, max_length=2)
    contact_email: EmailStr

    @field_validator("official_name", "registration_number")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("country_code")
    @classmethod
    def normalize_country(cls, value: str) -> str:
        return value.upper()


class NGORead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    official_name: str
    registration_number: str
    country_code: str
    contact_email: EmailStr
    created_at: datetime


class GrantCreate(BaseModel):
    title: str = Field(min_length=2, max_length=240)
    funder: str = Field(min_length=2, max_length=200)
    official_source_url: HttpUrl
    deadline: datetime | None = None


class GrantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    tenant_id: uuid.UUID
    title: str
    funder: str
    official_source_url: str
    status: str
    deadline: datetime | None
    created_at: datetime


class OpportunityIngest(BaseModel):
    source_identifier: str = Field(min_length=1, max_length=240)
    source_key: str = Field(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$")
    content_hash: str = Field(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$")
    title: str = Field(min_length=2, max_length=240)
    funder: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=2, max_length=20_000)
    eligibility: list[str] = Field(min_length=1, max_length=100)
    official_source_url: HttpUrl
    deadline: datetime | None = None
    timezone: str = Field(min_length=1, max_length=64)
    provenance: dict[str, object]
    observed_at: datetime


class OpportunityMatchIn(BaseModel):
    tenant_id: uuid.UUID
    opportunity_id: uuid.UUID
    score: int = Field(ge=0, le=100)
    factors: list[dict[str, object]] = Field(default_factory=list, max_length=50)
    missing_information: list[str] = Field(default_factory=list, max_length=100)
    exclusion_risks: list[str] = Field(default_factory=list, max_length=100)
    requires_human_review: Literal[True] = True
    model_provider: str = Field(min_length=2, max_length=80)
    model_id: str = Field(min_length=2, max_length=120)
    prompt_version: str = Field(min_length=1, max_length=40)


class ErrorResponse(BaseModel):
    detail: str
