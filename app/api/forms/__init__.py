from .blueprint import BluePrintTermsForm,BlurPrintForm
from pydantic import BaseModel, Field
from typing_extensions import Optional, List
from enum import Enum

## forms related to user start

class UserSignupForm(BaseModel):
    public_address: str = Field(..., description=" user Public address")
    username: str = Field(..., description=" user username")
    display_image: str = Field(..., description=" user display image")
    about: str = Field(..., description=" user about this user")


class UserLogin(BaseModel):
    public_address: str = Field(..., description="user wallet public address")


class UserProfileUpdate(BaseModel):
    about: Optional[str] = Field(..., description="user updated description")
    image_url: Optional[str] = Field(..., description="user updated image url")
    public_address: str = Field(..., description="user wallet public address")

## forms related to user end



