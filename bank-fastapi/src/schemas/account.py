from pydantic import BaseModel, PositiveFloat, Field, field_validator


class AccountIn(BaseModel):
    user_id: int = Field(..., gt=0, example=123)
    balance: PositiveFloat = Field(..., example=100.0)

    @field_validator('user_id')
    @classmethod
    def user_id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('user_id deve ser positivo')
        return v

    @field_validator('balance')
    @classmethod
    def balance_must_be_reasonable(cls, v):
        if v > 1000000:
            raise ValueError('balance muito alto')
        return v
