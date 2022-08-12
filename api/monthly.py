from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel, validator
from decimal import Decimal
from typing import Optional
from functools import reduce
import json
from re import compile
from datetime import datetime

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

class Months(Enum):
    JAN = 'JAN'
    FEB = 'FEB'
    MAR = 'MAR'
    APR = 'APR'
    MAY = 'MAY'
    JUN = 'JUN'
    JUL = 'JUL'
    AUG = 'AUG'
    SEP = 'SEP'
    OCT = 'OCT'
    NOV = 'NOV'
    DEC = 'DEC'
    
class MonthlyTransaction(BaseModel):
    alias: str
    control_number: str
    month: str
    year: int
    total_days: int
    total_payment: Decimal
    payment_per_day: list[Optional[Decimal]]
    accum_pay_per_day: list[Optional[Decimal]]

    @validator("payment_per_day", pre=True)
    def clean(cls, v, field):
        return [normalize_amount(x) if x else None for x in v]

    def __init__(self, **kwargs):
        total_payment = sum(
            [normalize_amount(d) for d in kwargs["payment_per_day"] if d]
        )
        total_days = len(kwargs["payment_per_day"])
        kwargs["total_payment"] = total_payment
        kwargs["total_days"] = total_days
        
        accum_days = []
        for days_amt in kwargs['payment_per_day']:
            this_day_not_null = normalize_amount(days_amt) or 0
            if accum_days:
                last_day_not_null = normalize_amount(accum_days[-1]) or 0
            else:
                last_day_not_null = 0
                
            accum_days.append(last_day_not_null + this_day_not_null)

                    
        kwargs['accum_pay_per_day'] = accum_days
        super().__init__(**kwargs)

def validate_month_name(month: str):
    '''see assumptions ##valid-months-name for the valid pattern'''
    pattern = compile(r'(\w+)((?:\s)\d{2,4})?')
    matches = pattern.fullmatch(month)
    
    if not matches:
        return False

    month_, year_ = matches.groups()
        
    yyear = datetime.now().year
    if year_:
        yyear = int( year_ )
        if yyear < 2020:
            return False
    
    if month_[:3].upper() in Months.__members__:
        return [month_[:3].upper(), yyear ]
    
    return False

@app.post('/api/monthly')
async def some_data(data: str , sheet: str)-> list[MonthlyTransaction]:
    monthly_values = json.loads(data)[3:]
    monthly_transactions = []
    for client_data in monthly_values:
        (
            _,
            alias,
            control_number,
            _,
            _,
            _,
            _,
            payed,
            _,
            _,
            _,
            _,
            _,
            *payment_per_day,
        ) = client_data
        month , _year = validate_month_name(sheet)
        monthly_transactions.append(
            MonthlyTransaction(
                alias=alias,
                control_number=control_number,
                payment_per_day=payment_per_day,
                month=month,
                year=int(_year),
            )
        )
    return monthly_transactions
