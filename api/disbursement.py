from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel, validator
from decimal import Decimal
from typing import Optional
from functools import reduce
from datetime import datetime, date as Date

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

    
class Disburser(BaseModel):
    alias: str
    full_name: str
    control_no: str
    type: str
    location: str
    released_date: Optional[Date]
    borrowed: Optional[Decimal]
    pf: Optional[Decimal]
    penalty: Optional[Decimal]
    gross_recv: Optional[Decimal]
    discountable: Optional[Decimal]
    net_recv: Optional[Decimal]
    status: str
    active_days: str
    paid_date: str
    days_paid: str
    terms: str
    completion_offset: str
    remarks: str

    @validator("released_date", pre=True)
    def parse_date(cls, value):
        if isinstance(value, Date):
            return value
        try:
            format = "%A, %B %d, %Y "
            parsed = datetime.strptime(value, format).date()
            return parsed
        except Exception as ex:
            print(f"Error Parsing Date => {ex}")
            return None

    @validator(
        "borrowed", "pf", "penalty", "gross_recv", "discountable", "net_recv", pre=True
    )
    def clean(cls, v, field):
        return normalize_amount(v)


class Body(BaseModel):
    data: str
    
@app.post('/api/monthly')
async def some_data(body: Body):
    try:   
        cached_disbursement = []
        for row in body.data[2:]:
            data = {
                key: value
                for key, value in zip(Disburser.schema()["properties"], row)
            }
            cached_disbursement.append(Disburser(**data))
            
    except Exception as e:
        return {"error": str(e)}
