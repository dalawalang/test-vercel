from fastapi import FastAPI
from pydantic import BaseModel, validator
from decimal import Decimal
from typing import Optional
from functools import reduce
from datetime import datetime, date as Date
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

    
class Disburser(BaseModel):
    alias: str
    full_name: str
    control_no: str
    type: str
    location: str
    released_date: str
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

    @validator(
        "borrowed", "pf", "penalty", "gross_recv", "discountable", "net_recv", pre=True
    )
    def clean(cls, v, field):
        return normalize_amount(v)


class Body(BaseModel):
    data: str
    
@app.post('/api/disbursement')
async def some_data(body: Body):
    try:
        data = json.loads(body.data) 
        cached_disbursement = []
        
        for row in data[2:]:
            try:
                content = {
                    key: value
                    for key, value in zip(Disburser.schema()["properties"], row)
                }
                
                bursement = Disburser(**content)
                if bursement.control_no:
                    cached_disbursement.append(bursement)
            except Exception as e:
                pass
            
        return cached_disbursement
            
    except Exception as e:
        return {"error": str(e)}
