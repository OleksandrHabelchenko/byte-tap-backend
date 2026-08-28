import sqlite3

import time


conn = sqlite3.connect('byte_tap.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                    telegram_id INTEGER PRIMARY KEY,
                    balance INTEGER DEFAULT 0,
                    tap_power INTEGER DEFAULT 1,
                    energy INTEGER DEFAULT 1000,
                    max_energy INTEGER DEFAULT 1000
                )''')

try:
    cursor.execute('ALTER TABLE players ADD COLUMN last_update INTEGER DEFAULT 0')
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()


def create_player(telegram_id):
    conn = sqlite3.connect('byte_tap.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO players (telegram_id, last_update) VALUES (?, ?)', (telegram_id, int(time.time())))
    conn.commit()
    conn.close()

def get_player(telegram_id):
    conn = sqlite3.connect('byte_tap.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players WHERE telegram_id = ?', (telegram_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_balance(telegram_id, new_balance):
    conn = sqlite3.connect('byte_tap.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET balance = ? WHERE telegram_id = ?', (new_balance, telegram_id))
    conn.commit()
    conn.close()

def update_after_tap(telegram_id, new_balance, new_energy, last_update):
    conn = sqlite3.connect('byte_tap.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET balance = ?, energy = ?, last_update = ? WHERE telegram_id = ?', (new_balance, new_energy, last_update, telegram_id))
    conn.commit()
    conn.close()


def get_current_energy(player):
    telegram_id, balance, tap_power, energy, max_energy, last_update = player

    seconds_passed = int(time.time()) - last_update
    regen_rate = 1  # Energy regenerated per second
    restored_energy = energy + seconds_passed * regen_rate
    if restored_energy > max_energy:
        restored_energy = max_energy
    return restored_energy


def update_energy_and_time(telegram_id, new_energy):
    conn = sqlite3.connect('byte_tap.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET energy = ?, last_update = ? WHERE telegram_id = ?', (new_energy, int(time.time()), telegram_id))
    conn.commit()
    conn.close()


def apply_taps(telegram_id, tap_count):
    player = get_player(telegram_id)
    telegram_id, balance, tap_power, energy, max_energy, last_update = player

    current_energy = get_current_energy(player)
    max_possible_taps = current_energy // tap_power
    actual_taps = min(tap_count, max_possible_taps)

    new_balance = balance + actual_taps * tap_power
    new_energy = current_energy - actual_taps * tap_power

    update_after_tap(telegram_id, new_balance, new_energy, int(time.time()))

    return new_balance, new_energy, actual_taps