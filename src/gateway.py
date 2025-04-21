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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db_interface import cast

DESCRIPTION: str = """
A basic ASGI for CRUD on a database of tasks 

# Clients

You will be able to:

* Retrieve tasks
* Update tasks 
* Delete tasks 
"""

app: FastAPI = FastAPI(title='Crud on tasks database',
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
ACCEPTED: int = cast(typ=int, val=http.HTTPStatus.ACCEPTED.value)
NOT_FOUND: int = cast(typ=int, val=http.HTTPStatus.NOT_FOUND.value)
