import os
import random
import asyncio
import httpx
import json
import aiosqlite
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_NAME= "stocks.db"



async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS stock_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                ticker TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        await db.commit()

@app.on_event ("startup")
async def startup_event():
    await init_db()



stocks = {
    "BRR": {"name": "BearCoin", "price": 28.0},
    "REKE": {"name": "Reketherium", "price": 42.0},
    "BGI": {"name": "Bear Group Inc.", "price": 230.0},
    "BEM": {"name": "Bearerium", "price": 550.0},
    "REG": {"name": "Reketino Group", "price": 333.0},
    "REP": {"name": "Reketino Portfolio", "price": 786.0},
}

# Github aksje som følger mine github contributions
def calculate_reketino_price(old_price, streak, commits_today, weekly_diff):
    change = 0

    change += random.uniform(-0.5, 0.5)
    change += streak * 0.05
    change += commits_today * 0.1
    change += weekly_diff * 0.0001

    new_price = old_price + change

    if new_price < 0.1:
        new_price = 0.1

    return round(new_price, 2)

# Alder aksjen min som teller ned til jeg har bursdag
def calculate_bearcoin_price(old_price):
    birthday_day = 30
    birthday_month = 9

    today = date.today()
    this_year_birthday = date(today.year, birthday_month, birthday_day)

    if today > this_year_birthday:
        this_year_birthday = date(today.year + 1, birthday_month, birthday_day)

    days_to_birthday = (this_year_birthday - today).days

    # extra boost når det nærmer seg
    if days_to_birthday <= 1: # 1 dag til bursdag boost
        boost = 0.20
    elif days_to_birthday <= 7: # 7 dager til bursdag boost
        boost = 0.01
    elif days_to_birthday <= 14: # 14 dager til bursdag boost
        boost = 0.004
    elif days_to_birthday <= 30: # 30 dager til bursdag boost
        boost = 0.001
    else:
        boost = 0.0002 # liten boost ellers


    volatility = random.uniform(-0.01, 0.01)


    new_price = old_price * (1 + boost + volatility)

    if new_price < 0.1:
        new_price = 0.1

    return round(new_price, 2)



async def fetch_github_data():
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        return {
            "total": 0,
            "commits_today": 0,
            "streak": 0
        }


    query = """
    query {
      user(login: "Reketino") {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
            contributionDays {
            date
            contributionCount
            }
            }
          }      
        } 
      }
    }
    """

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(
            "https://api.github.com/graphql",
            json={"query": query},
            headers=headers
        )
        data = response.json()
        total = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        days = []
        for week in weeks:
            for day in week["contributionDays"]:
                days.append(day)

        today = datetime.utcnow().strftime("%Y-%m-%d")

        commits_today = 0
        for d in days:
            if d["date"] == today:
                commits_today = d["contributionCount"]
                break

        days.sort(key=lambda x: x["date"])

        streak = 0 
        for d in reversed(days):
            if d["contributionCount"] > 0:
                streak += 1
            else:
                break
        return {"total": total,
                "commits_today": commits_today,
                "streak": streak
                }
    
@app.get("/history/{ticker}")
async def get_history(ticker: str):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT timestamp, price FROM stock_history WHERE ticker = ? ORDER BY id ASC",
            (ticker,)
        )
        rows = await cursor.fetchall()

    
    return [{"timestamp": r[0], "price": r[1]} for r in rows]

@app.websocket("/ws")
async def stream(ws: WebSocket):
    await ws.accept()

    while True:
        github_data = await fetch_github_data()


        for ticker, data in stocks.items():  


            if ticker == "REP": 
                data["price"] = calculate_reketino_price(
                    data["price"],
                    github_data["streak"],
                    github_data["commits_today"],
                    github_data["total"]
                 )
            
            elif ticker == "BRR":
                data["price"] = calculate_bearcoin_price(data["price"])
                
            else:
                data["price"] = round(data["price"] + random.uniform(-1,1), 2)

        
        await ws.send_json(stocks)


        timestamp = datetime.utcnow().isoformat()


        async with aiosqlite.connect(DB_NAME) as db:
            for ticker, data in stocks.items():
                await db.execute(
                    "INSERT INTO stock_history (timestamp, ticker, price) VALUES (?, ?, ?)",
                    (timestamp, ticker, data ["price"])
                )
            await db.commit()
        


        await asyncio.sleep(1)