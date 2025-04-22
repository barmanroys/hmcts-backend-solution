#!/usr/bin/env python3
# encoding: utf-8

"""
Asynchronous gateway interface to expose the Crud Application

For development, start it by
    $ uvicorn gateway:webapp --host=0.0.0.0 --port=8080 --reload

Skip the reload option above in containerised production environment to exploit
concurrent processing and withstand moderate user traffic.

Author: Barman Roy, Swagato
"""
import http
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from db_interface import cast, Task, InterfaceFactory, Optional, AbstractPersistenceInterface, pl, os

DESCRIPTION: str = """
A basic ASGI for CRUD on a database of tasks 

# Clients

You will be able to:

* Retrieve tasks
* Update tasks 
* Delete tasks 
"""

app: FastAPI = FastAPI(title='CRUD on tasks database',
                       description=DESCRIPTION,
                       contact=dict(name='Barman Roy, Swagato',
                                    email='swagatopablo@aol.com'))
origins = ['*']
app.add_middleware(middleware_class=CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=origins,
                   allow_headers=origins)

FAILURE: int = cast(typ=int, val=http.HTTPStatus.BAD_REQUEST.value)
CREATED: int = cast(typ=int, val=http.HTTPStatus.CREATED.value)
DELETED: int = cast(typ=int, val=http.HTTPStatus.NO_CONTENT.value)


@app.post(path='/create_task/', status_code=CREATED)
async def create_task(task: Task) -> None:
    """Persist a new task in the database."""
    db_client: AbstractPersistenceInterface = InterfaceFactory().get_sql_client()
    db_client.create_task(task=task)


@app.post(path='/retrieve_tasks/')
async def retrieve_tasks(tasks: Optional[List[int]] = None) -> str:
    """Retrieve the tasks in the form of a JSON."""
    db_client: AbstractPersistenceInterface = InterfaceFactory().get_sql_client()
    result: pl.DataFrame = await db_client.retrieve_tasks(tasks=tasks or None).collect_async()
    return result.write_json()


@app.post(path='/update_status/')
async def update_status(task: int, new_status: str) -> None:
    """Update the status of a task."""
    db_client: AbstractPersistenceInterface = InterfaceFactory().get_sql_client()
    db_client.update_status(task=task, new_status=new_status)


@app.delete(path='/delete_task/', status_code=DELETED)
async def delete_task(task: int) -> None:
    """Delete a task."""
    db_client: AbstractPersistenceInterface = InterfaceFactory().get_sql_client()
    db_client.delete_task(task=task)


if __name__ == '__main__':
    file: str = os.path.basename(p=__file__).split(sep='.')[0]
    appname: str = f'{file}:app'
    run(app=appname, host='0.0.0.0', port=8080, reload=True)
