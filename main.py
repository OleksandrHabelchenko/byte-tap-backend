from fastapi import FastAPI

from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware

from database import get_current_energy,apply_taps

import time

from database import create_player, get_player, update_after_tap, update_energy_and_time

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Byte Tap API запущен"}

@app.get("/game")
def game():
    return FileResponse("byte-tap.html")

@app.get("/player/{telegram_id}")
def get_or_create_player(telegram_id: int):
    create_player(telegram_id)
    player = get_player(telegram_id)
    
    current_energy = get_current_energy(player)
    update_energy_and_time(telegram_id, current_energy)
    
    return {
        "telegram_id": player[0],
        "balance": player[1],
        "tap_power": player[2],
        "energy": current_energy,
        "max_energy": player[4]
    }


@app.post("/player/{telegram_id}/tap")
def tap(telegram_id: int):
    player = get_player(telegram_id)
    current_energy = get_current_energy(player)
    if current_energy < player[2]:  # Check if the player has energy
        return {"error": "Not enough energy to tap"}
    else:
        
        new_balance = player[1] + player[2]
        new_energy = current_energy - player[2]
        update_after_tap(telegram_id, new_balance, new_energy, int(time.time()))
        return {
            "telegram_id": player[0],
            "new_balance": new_balance,
            "new_energy": new_energy
        }

@app.post("/player/{telegram_id}/tap-batch")
def tap_batch(telegram_id: int, taps: int):
    new_balance, new_energy, actual_taps = apply_taps(telegram_id, taps)
    return {
        "telegram_id": telegram_id,
        "new_balance": new_balance,
        "new_energy": new_energy,
        "actual_taps": actual_taps
    }