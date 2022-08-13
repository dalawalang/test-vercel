from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from re import compile

app = FastAPI()

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
    

class ValidMonth(BaseModel):
    month: str
    year: int
    sheet: str

class Body(BaseModel):
    sheetlist: list[str]
    
def validate_month_name(month: str):
    '''see assumptions ##valid-months-name for the valid pattern'''
    pattern = compile(r'(\w+)((?:\s)\d{2,4})?')
    matches = pattern.fullmatch(month)
    
    if not matches:
        return False

    month_, year_ = matches.groups()
        
    yyear = datetime.now().year
    if year_:
        if len(year_) == 2:
            yyear = 2000 + int(year_)
        else:
            yyear = int( year_ )
        if yyear < 2020:
            return False
    
    if month_[:3].upper() in Months.__members__:
        return ValidMonth(month=month_[:3].upper(), year=yyear , sheet=month)
    
    return False
    
@app.post('/api/validmonths')
async def some_data(body: Body)-> list[ValidMonth]:
    '''verifies list of sheet name'''
    try:
        valid_months = []
        for sheet_name in body.sheetlist:
            result = validate_month_name(sheet_name)
            if result:
                valid_months.append(result)

        return valid_months

    except Exception as e:
        return {"error": str(e)}
    