from pydantic import BaseModel, Field

class AddUserRequest(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=15, description="Username")
    user_password: str = Field(..., min_length=3, max_length=15, description="Password")
