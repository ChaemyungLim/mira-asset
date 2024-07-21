from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List
import yfinance as yf
import json

app = FastAPI()


def get_yf_stockprice(stock_code: str) -> List[Dict[str, Any]]:
    ticker = yf.Ticker(f'{stock_code}.KS')
    df = ticker.history(
        interval='1d',
        start='2022-01-01',
        actions=True,
        auto_adjust=True
    )
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    result = []
    for index, row in df.iterrows():
        result.append({
            'date': row['Date'],
            'Open': row['Open'],
            'High': row['High'],
            'Low': row['Low'],
            'Close': row['Close'],
            'Volume': row['Volume'],
            'Dividends': row['Dividends'],
            'Stock Splits': row['Stock Splits']
        })
    return result


@app.get("/stockprice")
def stockprice(stock_code: str):
    if not stock_code:
        raise HTTPException(status_code=400, detail="Missing stock_code parameter")
    
    try:
        data = get_yf_stockprice(stock_code)
        return {"items": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)