from flet import GestureDetector, MouseCursor, Container, DragEndEvent, DragStartEvent, DragUpdateEvent

# логгер
from constants import logger

CARD_WIDTH = 70
CARD_HEIGTH = 100
DROP_PROXIMITY = 20
CARD_OFFSET = 10


class Card(GestureDetector):
    """
    Аналогично Slot классу, давайте создадим новый Cardкласс со slotсвойством запоминать,
    в каком слоте он находится.
    Он будет наследоваться от GestureDetector, и мы переместим в него все методы, связанные с карточками
    """
    def __init__(self, solitaire, color):
        super().__init__()
        self.slot = None
        self.mouse_cursor = MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop
        self.left = None
        self.top = None
        self.solitaire = solitaire
        self.color = color
        self.content = Container(bgcolor=self.color, width=CARD_WIDTH, height=CARD_HEIGTH)

    def move_on_top(self):
        """Перемещает перетаскиваемую карту наверх стопки."""
        draggable_pile = self.get_draggable_pile()
        for card in draggable_pile:
            self.solitaire.controls.remove(card)
            self.solitaire.controls.append(card)
        self.solitaire.update()

    def bounce_back(self):
        """Returns card to its original position"""
        draggable_pile = self.get_draggable_pile()
        for card in draggable_pile:
            card.top = card.slot.top + card.slot.pile.index(card) * CARD_OFFSET
            card.left = card.slot.left
        self.solitaire.update()

    def place(self, slot):
        """
        Когда карта помещается в слот метода card.place(), нам нужно сделать три вещи:

        Извлеките карту из исходного слота, если она существует.
        Измените слот карты на новый слот
        Добавьте карту в стопку нового слота.
        :param slot: Текущий слот
        """

        draggable_pile = self.get_draggable_pile()
        for card in draggable_pile:
            # При обновлении карты top и left ее позиции leftдолжны оставаться прежними,
            # но topбудут зависеть от длины стопки нового слота
            card.top = slot.top + len(slot.pile) * CARD_OFFSET
            card.left = slot.left

            # Извлечение карты из текущего слота если она есть
            if card.slot:
                card.slot.pile.remove(card)

            # Изменение слот карты на новый слот
            card.slot = slot

            # добавление карты в новую кучу слотов
            slot.pile.append(card)

        self.solitaire.update()

    def start_drag(self, e: DragStartEvent):
        self.move_on_top()
        self.update()

    def drag(self, e: DragUpdateEvent):
        draggable_pile = self.get_draggable_pile()
        for card in draggable_pile:
            card.top = max(0, int(self.top) + int(e.delta_y)) + draggable_pile.index(card) * CARD_OFFSET
            card.left = max(0, int(self.left) + int(e.delta_x))
            card.update()

    def drop(self, e: DragEndEvent):
        for slot in self.solitaire.slots:
            if (
                    abs(self.top - slot.top) < DROP_PROXIMITY
                    and abs(self.left - slot.left) < DROP_PROXIMITY
            ):
                self.place(slot)
                self.update()
                return

        self.bounce_back()
        self.update()

    def get_draggable_pile(self):
        """возращает список карт в текущем слоте"""
        if self.slot:
            return self.slot.pile[self.slot.pile.index(self):]
        return [self]
