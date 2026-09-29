from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class HomeItem(BaseModel):
    category: str
    quantity: int = Field(default=1, ge=1, le=50)
    notes: str = ""
class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    city: str = Field(default="Chennai", min_length=2, max_length=100)
    style: str = "Modern"
    rooms: list[str] = Field(default_factory=list)
    items: list[HomeItem] = Field(default_factory=list)
class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = "Home"
    city: str = Field(default="Chennai", min_length=2, max_length=100)
    preferences: str = ""
class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=2, max_length=80)
    style: str = "Elegant"
    metal: str = "Any"
    outfit_color: str = ""
    notes: str = ""
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
class RecommendationItem(BaseModel):
    name: str
    category: str
    estimated_price: float
    platform: str
    search_url: str
    reason: str
    budget_share: float = 0
class RecommendationResponse(BaseModel):
    planner: str
    title: str
    summary: str
    total_budget: float
    estimated_total: float
    remaining_budget: float
    tips: list[str]
    recommendations: list[RecommendationItem]
    ai_powered: bool
    history_id: Optional[int] = None
