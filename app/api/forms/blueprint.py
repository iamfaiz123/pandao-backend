from uuid import UUID
from pydantic import BaseModel, Field
from typing_extensions import Optional, List
from enum import Enum


class ValueType(Enum):
    INT = "INT"
    DECIMAL = "DECIMAL"
    STRING = "STRING"


class ManiFestArgsForm(BaseModel):
    key: str = Field(..., description="key to replace in transaction manifest")
    value: ValueType = Field(..., description="type of the value")


class DeployManifestForm(BaseModel):
    mainfest: str = Field(..., description="deploy manifest of the form")
    manifest_args: List[ManiFestArgsForm] = Field(description="args for the manifest")


class BluePrintTermsForm(BaseModel):
    term: str = Field(..., description="The heading  of the blueprint")
    description: str = Field(..., description="The description of the blueprint")


class BlurPrintForm(BaseModel):
    slug: str = Field(..., description="slug of the blue print", example='blue-print')
    description: str = Field(..., description="description of the blue print")
    price: float = Field(..., description="price of the blue print")
    package_address: str = Field(..., description="package address of the blue print")
    terms: List[BluePrintTermsForm]
    deploy_manifest: DeployManifestForm



