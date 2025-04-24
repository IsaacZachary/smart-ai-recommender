from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class QueryType(str, Enum):
    COMPARATIVE = "comparative"
    FEATURE_BASED = "feature_based"
    SUBJECTIVE = "subjective"

class ProductSpec(BaseModel):
    key: str
    value: str

class Price(BaseModel):
    value: float
    currency: str = "KES"

class Product(BaseModel):
    name: str = Field(..., max_length=120)
    description: str = Field(..., max_length=250)
    specs: List[ProductSpec]
    image_url: HttpUrl
    price: Price
    vendor_url: HttpUrl
    confidence_score: float = Field(..., ge=0, le=1)

class RecommendationRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None
    language: Optional[str] = None

class RecommendationResponse(BaseModel):
    clarification: Optional[str] = None
    products: List[Product]
    session_id: str
    query_type: QueryType

class TipRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+254[0-9]{9}$")
    amount: float = Field(..., ge=10, le=5000)

class TipResponse(BaseModel):
    transaction_id: str
    status: str
    message: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: int 