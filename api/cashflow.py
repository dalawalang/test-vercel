from fastapi import FastAPI
from pydantic import BaseModel, validator
from decimal import Decimal
from typing import Optional
from functools import reduce
from datetime import datetime
import json

app = FastAPI()

def normalize_amount(amount: str)-> Decimal:
    '''normalize an amount of string or Decimal to Decimal'''
    remove_chars = [","]
    if not amount:return None
    if isinstance(amount, Decimal):return amount
    if isinstance(amount, str):
        reduced = reduce(lambda accum, next_value: accum.replace(next_value,'') , [amount , *remove_chars])
        return Decimal(reduced)
    return Decimal(amount)

def date_parser(date_str: str):
    format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(date_str, format).date()

    
class Cashflow(BaseModel):
    date: str
    daily_let: Optional[Decimal]
    placehoder: Optional[Decimal]
    daily_irene: Optional[Decimal]
    releases_from_col: Optional[Decimal]
    releases_from_greg: Optional[Decimal]
    releases_to_irene: Optional[Decimal]
    expenses_from_col: Optional[Decimal]
    expenses_from_greg: Optional[Decimal]
    bank_depot_let: Optional[Decimal]
    bank_depot_greg: Optional[Decimal]
    place_hoder: Optional[Decimal]
    remmitance: Optional[Decimal]
    capital: Optional[Decimal]
    withrawals_to_greg: Optional[Decimal]

    @validator("*", pre=True)
    def clean(cls, v, field):
        if field.name == "date":
            return v
        return normalize_amount(v)



class Body(BaseModel):
    data: str
    
@app.post('/api/cashflow')
async def some_data(body: Body):
    today = datetime.now().date()
    try:
        data = json.loads(body.data) 
        cached_cashflow = []
        
        for row in data[4:]:
            label: dict[str, any] = {}
            for key, value in zip(Cashflow.schema()["properties"], row[:15]):
                label[key] = value
                
            _cashflow_data = Cashflow(**label)
            if date_parser(_cashflow_data.date) <= today:
                cached_cashflow.append(_cashflow_data)

        return cached_cashflow
            
    except Exception as e:
        return {"error": str(e)}
