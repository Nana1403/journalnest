"""Pydantic schemas for structured JSON requests.

These validate the *shape* of autosave and customization payloads. They are
not a substitute for authentication or per-object ownership checks — the views
still confirm ``request.user`` owns the notebook/note before touching it.
"""

import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .constants import (
    COLOR_CHOICES,
    FONT_CHOICES,
    PATTERN_CHOICES,
    TYPE_CHOICES,
    values,
)

ColorValue = Literal[tuple(values(COLOR_CHOICES))]  # type: ignore[valid-type]
PatternValue = Literal[tuple(values(PATTERN_CHOICES))]  # type: ignore[valid-type]
FontValue = Literal[tuple(values(FONT_CHOICES))]  # type: ignore[valid-type]
TypeValue = Literal[tuple(values(TYPE_CHOICES))]  # type: ignore[valid-type]


class AutosavePayload(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    content: str = Field(max_length=100_000)
    revision: int = Field(ge=0)


class Sticker(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sticker: str = Field(min_length=1, max_length=32)
    x: float = Field(ge=0, le=100)
    y: float = Field(ge=0, le=100)
    rotation: float = Field(ge=-180, le=180)


class NotebookCustomization(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    label: str = Field(min_length=1, max_length=120)
    label_font: FontValue
    cover_color: ColorValue
    cover_pattern: PatternValue
    notebook_type: TypeValue
    sticker_layout: list[Sticker] = Field(default_factory=list, max_length=40)


class SchemaError(Exception):
    """Raised when a request body is missing, not JSON, or fails validation."""

    def __init__(self, errors):
        self.errors = errors
        super().__init__("Invalid request payload")


def parse_body(request, schema: type[BaseModel]) -> BaseModel:
    """Validate ``request.body`` against ``schema`` or raise ``SchemaError``."""
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        raise SchemaError([{"loc": ["body"], "msg": "Request body is not valid JSON"}])
    try:
        return schema.model_validate(data)
    except ValidationError as exc:
        raise SchemaError(exc.errors(include_url=False))
