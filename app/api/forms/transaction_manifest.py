import uuid
from uuid import UUID
from pydantic import BaseModel, Field
from typing_extensions import Optional, List
from enum import Enum


class TransactionSubmit(BaseModel):
    tx_id: str
    user_address: str


class DeployTokenWeightedDao(BaseModel):
    userAddress: str = Field(..., description="wallet address of user")
    communityName: str = Field(..., description="name of the community user want to create")
    tokenSupply: int = Field(..., description="token Supply")
    tokenPrice: float = Field(..., description="token price")
    tokenWithDrawPrice: float = Field(..., description="token withdraw price")
    communityImage: str = Field(..., description="community image")
    tokenImage: str = Field(..., description="token image")


class BuyTokenWeightedDaoToken(BaseModel):
    userAddress: str = Field(..., description="wallet address of user")
    # community_id: uuid = Field(..., description="id of the community user want buy token from")
    tokenSupply: int = Field(..., description="token Supply user want to buy")