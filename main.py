import os
import random
import asyncio
import httpx
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stocks = {
    "BRR": {"name": "BearCoin", "price": 28.0},
    "REKE": {"name": "Reketherium", "price": 42.0},
    "BGI": {"name": "Bear Group Inc.", "price": 230.0},
    "BEM": {"name": "Bearerium", "price": 550.0},
    "REG": {"name": "Reketino Group", "price": 333.0},
    "REP": {"name": "Reketino Portfolio", "price": 786.0},
}

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



async def fetch_github_data():
    token = os.getenv("GITHUB_TOKEN")

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
        # TODO: send request med httpx
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
            else:
                data["price"] = round(data["price"] + random.uniform(-1,1), 2)
        
        await ws.send_json(stocks)
        await asyncio.sleep(1)