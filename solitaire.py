import flet as ft
from slot import Slot
from card import Card

# from main import logger

SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500


class Solitaier(ft.Stack):
    """
    Класс предназначен для сохранение исходного положения карты
    """
    def __init__(self):
        super().__init__()
        self.controls = list()
        self.slots = list()
        self.cards = list()
        self.width = SOLITAIRE_WIDTH
        self.heigth = SOLITAIRE_HEIGHT

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def create_card_deck(self):
        list_cards = [
            Card(self, color="GREEN"),
            Card(self, color="YELLOW"),
            Card(self, color="BLUE"),
        ]
        self.cards = [card for card in list_cards]

    def create_slots(self):
        self.slots.append(Slot(top=0, left=0))
        self.slots.append(Slot(top=0, left=200))
        self.slots.append(Slot(top=0, left=300))
        self.controls.extend(self.slots)
        self.update()

    def deal_cards(self):
        self.controls.extend(self.cards)
        for card in self.cards:
            card.place(self.slots[0])
        self.update()
