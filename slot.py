from flet import Container, border

# логгер
from constants import logger

SLOT_WIDTH = 70
SLOT_HEIGHT = 100


class Slot(Container):
    """
    Слот может иметь pileсвойство, которое будет содержать список помещенных туда карт.
    Теперь слот является Containerобъектом управления, и мы не можем добавлять к нему новые свойства.
    Давайте создадим новый Slotкласс, который будет наследовать его Container, и добавим pileк нему свойство
    """
    def __init__(self, top, left):
        super().__init__()
        self.pile = list()
        self.width = SLOT_WIDTH
        self.height = SLOT_HEIGHT
        self.left = left
        self.top = top
        self.border = border.all(1)
