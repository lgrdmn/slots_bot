import random as r
import sqlite3

values_bonus = {
    '🍒': 2,
    '🍋': 4,
    '🍊': 8,
    '🍓': 15,
    '🍉': 30,
    '🍌': 50,
    '🔔': 150,
    '🎱': 200,
    '💎': 500
}


def creator_db():
    """ Создание базы данных игроков """
    conn = sqlite3.connect('slots_players.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS players(
    id INT PRIMARY KEY,
    credit INT,
    bet_size INT);
    """)
    conn.commit()
    conn.close()


def start_values(start_id):
    """ Данные для нового игрока """
    try:
        conn = sqlite3.connect('slots_players.db')
        cur = conn.cursor()
        start_credit = 40
        start_bet_size = 4
        values = [start_id, start_credit, start_bet_size]
        cur.execute("INSERT INTO players VALUES(?, ?, ?);", values)
        conn.commit()
        conn.close()
    except Exception as error:
        print(error)


def all_players():
    """ Загрузка всех игроков из базы данных """
    conn = sqlite3.connect('slots_players.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM players;")
    all_results = cur.fetchall()
    conn.close()
    return all_results


def add_values_to_db(player_id, add_credit, add_bet_size):
    """ Запись результата игры в базу данных игроков """
    try:
        conn = sqlite3.connect('slots_players.db')
        cur = conn.cursor()
        cur.execute("UPDATE players SET 'credit'=?, 'bet_size'=? WHERE 'id'=?;",
                    (add_credit, add_bet_size, player_id))
        conn.commit()
        conn.close()
    except Exception as error:
        print(error)


def up_balance(player_id):
    """ Пополнение баланса после обнуления """
    try:
        up_credit = 100
        up_bet_size = 5
        conn = sqlite3.connect('slots_players.db')
        cur = conn.cursor()
        cur.execute("UPDATE players SET 'credit'=?, 'bet_size'=? WHERE 'id'=?;",
                    (up_credit, up_bet_size, player_id))
        conn.commit()
        conn.close()
        return up_credit, up_bet_size
    except Exception as error:
        print(error)


def player_finder(player_id):
    """ Поиск данных игрока по id """
    try:
        conn = sqlite3.connect('slots_players.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM players WHERE id=?;", (player_id,))
        results = cur.fetchall()
        conn.close()
        return results
    except Exception as error:
        print(error)


def values_generator():
    """ Генератор значений слот-машины """
    keys = list(values_bonus.keys())
    return r.choice(keys), r.choice(keys), r.choice(keys)


def bonus(first_value, second_value, third_value):
    """ Определение размера умножения бонуса """
    size = 0
    if first_value == second_value == third_value:
        size = values_bonus[second_value]
    return size


def game(player_id):
    results = player_finder(player_id)
    print(results)
    game_credit = results[0][1]
    game_bet_size = results[0][2]
    slot1, slot2, slot3 = values_generator()
    bonus_size = bonus(slot1, slot2, slot3)
    print(game_credit, game_bet_size)
    game_credit -= game_bet_size
    print(game_credit, game_bet_size)
    win_size = bonus_size * game_bet_size
    game_credit += win_size
    print(game_credit, win_size)
    print(player_id, game_credit, game_bet_size)
    add_values_to_db(player_id, game_credit, game_bet_size)
    return slot1, slot2, slot3, win_size, player_id, game_credit, game_bet_size


