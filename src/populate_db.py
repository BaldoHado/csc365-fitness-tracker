from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from src.api import auth
import sqlalchemy
from src import database as db
from faker import Faker


def add_rows_users():
    return
