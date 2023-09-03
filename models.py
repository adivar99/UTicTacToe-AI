from pydantic import BaseModel, Field


class Position(BaseModel):
    board: int = Field(..., title="board number", example=5, gt=0, lt=10)
    row: int = Field(..., title="Row number", example=2, gt=0, lt=4)
    column: int = Field(..., title="Column number", example=1, gt=0, lt=4)