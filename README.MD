## 🐻 BearStocks – Live Meme-Coin Engine

Et realtime aksjemarked som simulerer crazy coins – inkludert to coins koblet til livet mitt: GitHub-aktivitet og bursdagen min.

BearStocks er en FastAPI-drevet backend med en WebSocket-strøm som kontinuerlig sender ut oppdaterte priser for seks fiktive coins i “BearWeb-universet”.

## 🚀 Features

## 🟦 Reketino Portfolio (REP)

En coin som er direkte koblet til GitHub-aktiviteten min:

Commits i dag → pump

Streak → bullrun

Ingen commits → dip

Total contributions → weak/strong trend

Dette er basically en AI-styrt meme-coin som lever i sanntid av hvor flink jeg er på GitHub.

## 🟧 BearCoin (BRR) – Bursdags-Bullrun™

BearCoin går opp i verdi jo nærmere jeg kommer bursdagen min.

Boosts:

Dager til bursdag	Effekt
30 dager	+0.1%/dag
14 dager	+0.4%/dag
7 dager	+1%/dag
1 dag	+20% burst
Bursdagen	Massiv mooning

Perfekt for en personlig coin som hyller at jeg blir eldre og visere 🧓🏻

## 🟩 Andre coins

De resterende coinene (BGI, REKE, REG, BEM) får små tilfeldige svingninger så markedet føles levende.

## ⚙️ Teknologier

Python 3.12

FastAPI

WebSockets

httpx (GitHub GraphQL API)

Uvicorn

Render (deployment)

Next.js / Tailwind (frontend - coming soon)

## 🔌 WebSocket Endpoint
URL
/ws

Response (hver 1 sekund)
{
  "BRR": {
    "name": "BearCoin",
    "price": 28.41
  },
  "REP": {
    "name": "Reketino Portfolio",
    "price": 789.55
  },
  ...
}

## 🧠 Hvordan prisene beregnes
REP (GitHub-basert)
price += random drift
price += streak * 0.05
price += commits_today * 0.1
price += total_contributions * 0.0001

BRR (Bursdags-bullrun)
price *= (1 + seasonal boost + volatility)

🛠 Kjøre prosjektet lokalt
pip install -r requirements.txt
uvicorn main:app --reload


Websocket kjører da på:

ws://localhost:8000/ws

## 🌐 Deployment (Render)

Push til GitHub

Lag en ny Web Service i Render

Legg til miljøvariabel:

GITHUB_TOKEN=<token>


Autodeploy

Ferdig 🚀

## 🎯 Videre planer

Full Next.js frontend med live charts

Flash crashes og moon-events

Admin dashboard

Logging av markedshendelser

Notifikasjoner

BearWeb OS-integrasjon