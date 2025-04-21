#!/usr/bin/env python3
# encoding: utf-8

"""This file presents the definition of a task."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator
from typing_extensions import FrozenSet

ALLOWED_STATUS: FrozenSet[str] = frozenset(('WIP', 'DONE', 'PENDING'))


# noinspection PyMethodParameters
class Task(BaseModel):
    """Define the class tasks with appropriate constraints on the field."""
    title: str
    description: Optional[str] = None
    status: str = 'PENDING'
    due: datetime

    @field_validator('title')
    def check_title(cls, value):
        """Ensure the title field valid."""
        if len(value) > 60:
            raise ValueError
        return value

    @field_validator('description')
    def check_description(cls, value):
        """Ensure the description field valid."""
        if isinstance(value, str) and len(value) > 500:
            raise ValueError
        return value

    @field_validator('status')
    def check_status(cls, value):
        """Ensure the status field valid."""
        if value not in ALLOWED_STATUS:
            raise ValueError
        return value
