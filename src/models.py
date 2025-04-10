from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class MountingType(str, Enum):
    WALL_HUNG = "wall_hung"
    FLOOR_MOUNTED = "floor_mounted"
    CEILING_MOUNTED = "ceiling_mounted"
    OTHER = "other"

class Dimension(BaseModel):
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    diameter: Optional[float] = None
    unit: str = "mm"

class ExtractedItem(BaseModel):
    item_type: str = Field(..., description="Type of fixture or component")
    quantity: int = Field(..., description="Number of items")
    model_number: Optional[str] = Field(None, description="Model number or specification reference")
    page_reference: int = Field(..., description="Page number where the item appears")
    dimensions: Optional[Dimension] = Field(None, description="Associated dimensions if available")
    mounting_type: Optional[MountingType] = Field(None, description="How the item is mounted")
    additional_notes: Optional[str] = Field(None, description="Any additional relevant information")

class ExtractionResult(BaseModel):
    items: List[ExtractedItem] = Field(..., description="List of extracted items")
    source_file: str = Field(..., description="Name of the source PDF file")
    extraction_date: str = Field(..., description="Date and time of extraction") 