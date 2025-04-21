#!/usr/bin/env python3
# encoding: utf-8

"""This file presents the abstract interface and implementation of a Database Client."""
import logging
import os
from abc import ABC, abstractmethod
from configparser import ConfigParser
from contextlib import AbstractContextManager
from typing import Iterable, cast, Any

import polars as pl
from sqlalchemy import create_engine, Engine, Table, MetaData, Delete, delete, Update, Insert
from sqlalchemy.orm import Session, Query

from task_def import Optional, ALLOWED_STATUS, Task

logging.basicConfig(format='%(asctime)s|%(levelname)s: %(message)s',
                    datefmt='%H:%M:%S, %d-%b-%Y', level=logging.DEBUG)

# Load basic configurations
config: ConfigParser = ConfigParser()
assert config.read(filenames='config.ini')

PRIM_KEY: str = config.get(section='columns', option='PRIM_KEY_COL')
TITLE: str = config.get(section='columns', option='TITLE')
DETAIL: str = config.get(section='columns', option='DETAIL')
STATUS: str = config.get(section='columns', option='STATUS')
DUE: str = config.get(section='columns', option='DUE')

DIALECT: str = config.get(section='db', option='DIALECT', raw=True)
DRIVER: str = config.get(section='db', option='DRIVER', raw=True)
DB_USERNAME: str = os.environ['USER']
DB_PASSWORD: str = os.environ['MYSQL_PASSWORD']
HOST: str = config.get(section='db', option='HOST', raw=True)
PORT: int = int(config.get(section='db', option='PORT', raw=True))
TABLE: str = config.get(section='db', option='TABLE', raw=True)
DATABASE: str = os.environ['MYSQL_DATABASE']
HOST_CONNECTOR = (f'{DIALECT}+{DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{HOST}:'
                  f'{PORT}')
URI: str = os.path.join(HOST_CONNECTOR, DATABASE)


class AbstractPersistenceInterface(ABC):
    """Define the interface to persist data."""

    @abstractmethod
    def create_task(self, task: Task) -> None:
        """Persist a new task in the database."""
        raise NotImplementedError

    @abstractmethod
    def retrieve_tasks(self, tasks: Optional[Iterable[int]] = None) -> pl.LazyFrame:
        """Retrieve a collection of tasks by task id or all tasks."""
        raise NotImplementedError

    @abstractmethod
    def update_status(self, task: int, new_status: str) -> None:
        """Update the status of a task by id."""
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task: int) -> None:
        """Delete a task."""
        raise NotImplementedError


class EngineContext(AbstractContextManager):
    """Wrap the connectivity engine inside a context to prevent leakage."""

    def __init__(self, uri: str):
        """
        Initialise the class with the connection string.
        Do not start the engine. Leave it to the context manager to acquire
        a connection.
        """
        self.uri: str = uri
        self.engine: Optional[Engine] = None

    def __enter__(self) -> Engine:
        """Create an engine and acquire the connection."""
        self.engine = cast(typ=Engine, val=create_engine(url=self.uri))
        logging.debug(msg=f'Engine created from {self.engine.url}.')
        return cast(typ=Engine, val=self.engine)

    def __exit__(self, exception_type: Any, exception_value: Any,
                 traceback: Any) -> None:
        """Release the connection."""
        self.engine.dispose()
        logging.debug(msg='Engine disposed.')


class DBInterface(AbstractPersistenceInterface):
    """Implement the asynchronous interface to the MySQL database."""

    def __init__(self, engine: EngineContext):
        """Initialise the client with an asynchronous engine."""
        self._engine_: EngineContext = engine

    def retrieve_tasks(self, tasks: Optional[Iterable[int]] = None) -> pl.LazyFrame:
        """Query the relevant tasks by task ids. If no task id supplied, get all tasks."""
        with self._engine_ as engine:
            session: Session = Session(bind=engine)
            table: Table = Table(TABLE, MetaData(), autoload_with=engine)
            query: Query = session.query(table.columns[PRIM_KEY], table.columns[TITLE], table.columns[DETAIL],
                                         table.columns[DUE],
                                         table.columns[STATUS])
            if tasks:
                query = query.filter(table.columns[PRIM_KEY].in_(other=tasks))
            raw_query: str = str(
                query.order_by(table.columns[DUE]).statement.compile(compile_kwargs={'literal_binds': True}))
            logging.debug(msg=f'Retrieving all tasks matching {tasks}.')
            return pl.read_database(query=raw_query, connection=session).lazy()

    def delete_task(self, task: int) -> None:
        """Delete a task by task id."""
        with self._engine_ as engine:
            table: Table = Table(TABLE, MetaData(), autoload_with=engine)
            with Session(bind=engine) as session, session.begin():
                stmt: Delete = delete(table=table).where(table.columns[PRIM_KEY] == task)
                logging.debug(msg=f'Deleting task id {task}.')
                session.execute(statement=stmt)

    def update_status(self, task: int, new_status: str) -> None:
        """Update the status of a task by task id."""
        try:
            assert new_status in ALLOWED_STATUS
        except AssertionError:
            message: str = f'Status {new_status} not allowed.'
            logging.error(msg=message)
            raise ValueError(message)
        with self._engine_ as engine:
            table: Table = Table(TABLE, MetaData(), autoload_with=engine)
            with Session(bind=engine) as session, session.begin():
                stmt: Update = table.update().where(table.columns[PRIM_KEY] == task).values(status=new_status)
                logging.debug(msg=f'Updating task {task} status to {new_status}.')
                session.execute(statement=stmt)

    def create_task(self, task: Task) -> None:
        """Persist a new task in the database."""
        with self._engine_ as engine:
            table: Table = Table(TABLE, MetaData(), autoload_with=engine)
            stmt: Insert = table.insert().values([dict(task)])
            with Session(bind=engine) as session, session.begin():
                session.execute(statement=stmt)


class InterfaceFactory:
    """Factory class to generate a persistence client"""

    @staticmethod
    def get_sql_client() -> AbstractPersistenceInterface:
        """Get the DBInterface"""
        return DBInterface(engine=EngineContext(uri=URI))
