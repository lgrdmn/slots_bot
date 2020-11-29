import random as r
import sqlite3


def deck():
    """ Генерация колоды карт """
    suits = ['♠', '♣', '♥', '♦']
    cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    deck_of_cards = []
    for i in suits:
        for j in cards:
            card = j + i
            deck_of_cards.append(card)
    return deck_of_cards


def cards_values():
    """ Генерация раздачи 5 карт """
    deck_of_cards = deck()
    five_cards = []
    for i in range(0, 5):
        card = r.choice(deck_of_cards)
        deck_of_cards.remove(card)
        five_cards.append(card)
    five_cards = tuple(five_cards)
    return five_cards


def check_flush(suits):
    """ Определение флэша """
    flushes = ['♠♠♠♠♠', '♣♣♣♣♣', '♥♥♥♥♥', '♦♦♦♦♦']
    flush = 0
    if suits in flushes:
        flush += 1
    return flush


def check_straight(values):
    """ Определение стрита """
    straights = [{'A', '2', '3', '4', '5'},
                 {'2', '3', '4', '5', '6'},
                 {'3', '4', '5', '6', '7'},
                 {'4', '5', '6', '7', '8'},
                 {'5', '6', '7', '8', '9'},
                 {'6', '7', '8', '9', 'T'},
                 {'7', '8', '9', 'T', 'J'},
                 {'8', '9', 'T', 'J', 'Q'},
                 {'9', 'T', 'J', 'Q', 'K'},
                 {'T', 'J', 'Q', 'K', 'A'}]
    straight = 0
    straight_values = set(values)
    if straight_values in straights:
        straight += 1
    return straight


def check_pairs(values):
    """ Определение одной или двух пар """
    one_pair = 0
    two_pair = 0
    values = list(values)
    for symbol in values:
        if values.count(symbol) == 2:
            one_pair += 1
            values.remove(symbol)
            if one_pair > 1:
                two_pair += 1
    return one_pair, two_pair


def check_three_of_a_kind(values):
    """ Определение тройки """
    three_of_a_kind = 0
    values = list(values)
    for symbol in values:
        if values.count(symbol) == 3:
            three_of_a_kind += 1
    return three_of_a_kind


def check_four_of_a_kind(values):
    """" Определение каре """
    four_of_a_kind = 0
    values = list(values)
    for symbol in values:
        if values.count(symbol) == 4:
            four_of_a_kind += 1
    return four_of_a_kind


def check_full_house(values):
    """ Определение фул-хауса """
    one_pair, two_pair = check_pairs(values)
    three_of_a_kind = check_three_of_a_kind(values)
    full_house = 0
    if one_pair == 1 and three_of_a_kind != 0:
        full_house += 1
    return full_house


def check_straight_flush(values):
    """ Определение стрит-флеша """
    straight = check_straight(values)
    flush = check_flush(values)
    straight_flush = 0
    if straight != 0 and flush != 0:
        straight_flush += 1
    return straight_flush


def check_royal_flush(values):
    """ Определение роял-флэша """
    straight = check_straight(values)
    flush = check_flush(values)
    royal_flush = 0
    if straight != 0 and flush != 0 and set(values) == {'T', 'J', 'Q', 'K', 'A'}:
        royal_flush += 1
    return royal_flush


def check_combination():
    """ Определение выпавшей комбинации"""
    message = 'Нет комбинации'
    card1, card2, card3, card4, card5 = cards_values()
    values = card1[0] + card2[0] + card3[0] + card4[0] + card5[0]
    suits = card1[1] + card2[1] + card3[1] + card4[1] + card5[1]
    print(card1, card2, card3, card4, card5)
    print(values, suits)
    one_pair, two_pair = check_pairs(values)
    three_of_a_kind = check_three_of_a_kind(values)
    straight = check_straight(values)
    flush = check_flush(values)
    full_house = check_full_house(values)
    four_of_a_kind = check_four_of_a_kind(values)
    straight_flush = check_straight_flush(values)
    royal_flush = 0
    if royal_flush != 0:
        message = 'Роял-Флэш'
    elif straight_flush != 0:
        message = 'Стрит-Флэш'
    elif four_of_a_kind != 0:
        message = 'Каре'
    elif full_house != 0:
        message = 'Фул-хаус'
    elif flush != 0:
        message = 'Флэш'
    elif straight != 0:
        message = 'Стрит'
    elif three_of_a_kind != 0:
        message = 'Тройка'
    elif two_pair != 0:
        message = 'Две пары'
    elif one_pair == 1:
        message = 'Одна пара'
    return message


print(check_combination())
