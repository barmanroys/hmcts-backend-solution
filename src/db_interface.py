#!/usr/bin/env python3
# encoding: utf-8

"""This file presents the abstract interface and implementation of a Database Client."""
from abc import ABC, abstractmethod
from typing import Iterable, Optional
import polars as pl

class AbstractPersistenceInterface(ABC):
    """Define the interface to persist data."""

    @abstractmethod
    async def retrieve_tasks(self, tasks:Optional[Iterable[int]|int]=None)->pl.DataFrame:
        """Retrieve a collection of tasks, a single task or all tasks."""
        raise NotImplementedError

    @abstractmethod
    async def update_status(self, task:int, new_status:str)->None:
        """Update the status of a task by id."""
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task:int)->None:
        """Delete a task."""
        raise NotImplementedError