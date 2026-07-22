from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Intent(str, Enum):
    AI_ANALYSIS = "AI_ANALYSIS"

    REMOVE_DUPLICATES = "REMOVE_DUPLICATES"
    REPLACE_NULL_VALUES = "REPLACE_NULL_VALUES"
    SORT_DATA = "SORT_DATA"

    RENAME_COLUMN = "RENAME_COLUMN"
    DELETE_COLUMN = "DELETE_COLUMN"
    FILTER_DATA = "FILTER_DATA"
    REPLACE_VALUES = "REPLACE_VALUES"
    UPDATE_CELL = "UPDATE_CELL"
    CREATE_NEW_COLUMN = "CREATE_NEW_COLUMN"

    CREATE_VISUALIZATION = "CREATE_VISUALIZATION"

    DOWNLOAD_DATASET = "DOWNLOAD_DATASET"


class ToolStep(BaseModel):
    intent: Intent
    parameters: dict[str, Any] = Field(default_factory=dict)


class AgentPlan(BaseModel):
    steps: list[ToolStep]
