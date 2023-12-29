# Логгер
from loguru import logger
import flet as ft

from os.path import abspath, join
# Константы
from constants import Constants

constants = Constants()
logger.remove()
logger.add(
    abspath(join('logs', '{time:YYYY-MM-DD  HH.mm.ss}.log')),  # Путь к файлу логов с динамическим именем
    rotation=constants.ROTATION_LOGGER,  # Ротация логов каждый день
    compression="zip",  # Использование zip-архива
    level=constants.LEVEL_FILE_LOGGER,  # Уровень логирования
    format=constants.FORMAT_LOGGER,  # Формат вывода
    serialize=constants.SERIALIZE_LOGGER,  # Сериализация в JSON
)

# Вывод лога в консоль
logger.add(
    sink=print,
    level=constants.LEVEL_CONSOLE_LOGGER,
    format=constants.FORMAT_LOGGER,
)


def main(page: ft.Page) -> None:
    SOLITAIRE_WIDTH = 1000
    SOLITAIRE_HEIGHT = 500
    class Solitaire:
        """
        Класс предназначен для сохранение исходного положения карты
        """
        def __init__(self):
            self.start_top = 0
            self.start_left = 0

    def drag(e: ft.DragUpdateEvent) -> None:
        """
        Чтобы иметь возможность перемещать карту, создается drag метод,
        который будет вызываться в on_pan_update случае события GestureDetector,
        которое происходит каждый drag_intervalраз,
        когда пользователь перетаскивает карту с помощью мыши.

        :param e: Объект обновления
        """

        # Обновляется top
        e.control.top = max(0, e.control.top + e.delta_y)
        # Обновляется left
        e.control.left = max(0, e.control.left + e.delta_x)
        # Для вступления обновлений в силу используется метод update()
        e.control.update()
        logger.debug(f'Update {e.control.top=} {e.control.left=}')

    def drop(e: ft.DragEndEvent) -> None:
        """
        Попала ли карта на слот?
        Если да, то обнолвение ее расположение
        Иначе вернуть на исходное место

        :param e: Объект проверки
        """
        max_pixel_top = 20  # Если ближе чем max_pixel_top пиксель, вставить в слот
        max_pixel_left = 20  # Если ближе чем max_pixel_left пиксель, вставить в слот
        for slot in slots:
            """Обход циклом все слоты"""
            if (
                    abs(e.control.top - slot.top) < max_pixel_top
                    and abs(e.control.left - slot.left) < max_pixel_left
            ):
                place(e.control, slot)
                logger.debug('Вставка в слот')
                return

        bounce_back(solitaire, e.control)
        logger.debug('Карту в исходное положение')
        e.control.update()

    def place(card_place: ft.GestureDetector, slot_place: ft.Container) -> None:
        """
        Присваивание раположению карты расположение слота

        :param card_place: расположение карты
        :param slot_place: расположение слота
        """
        card_place.top = slot_place.top
        card_place.left = slot_place.left
        page.update()
        logger.debug('Располжение карты приравнено к расположению слота')

    def bounce_back(game, card_: ft.GestureDetector) -> None:
        """
        Возращает расположение карты в исходное

        :param game: Стартовое расположение карты
        :param card_: Текущее расположение карты
        """
        card_.top = game.start_top
        card_.left = game.start_left
        page.update()
        logger.debug('Карта возращена в исходное положение')

    def start_drag(e: ft.DragStartEvent) -> None:
        """
        Сохранение исходного положения карты

        :param e: Карта
        """
        move_on_top(e.control, controls)
        solitaire.start_top = e.control.top
        solitaire.start_left = e.control.left
        e.control.update()
        logger.debug('исходное положение карты сохранено')

    def move_on_top(card_: ft.GestureDetector, controls_):
        """
        Перемещение активной карты в начало списка, чтобы карта была по верх остальных
        :param card_: карта
        :param controls_: список карт
        """
        controls_.remove(card_)
        controls_.append(card_)
        page.update()
        logger.debug("Активная карта перемещена в начало списка")

    # Карта пасьянса
    card0 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,  # Перетаскивание мышью
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,  # перемещение карты
        on_pan_end=drop,  # Проверка конечного расположение карты
        left=0,
        top=0,
        content=ft.Container(bgcolor=ft.colors.GREEN, width=70, height=100)
    )
    logger.debug('Карта создана')

    card1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=100,
        top=0,
        content=ft.Container(bgcolor=ft.colors.YELLOW, width=70, height=100),
    )
    logger.debug('Вторая карта добавлена')

    # Добавление слотов под карту
    slot0 = ft.Container(
        width=70, height=100, left=0, top=0, border=ft.border.all(1)
    )
    slot1 = ft.Container(
        width=70, height=100, left=200, top=0, border=ft.border.all(1)
    )
    slot2 = ft.Container(
        width=70, height=100, left=300, top=0, border=ft.border.all(1)
    )
    logger.debug('Слоты под карту добавлен')

    place(card0, slot0)
    place(card1, slot0)

    slots = [slot0, slot1, slot2]
    cards = [card0, card1]

    solitaire = Solitaire()

    # Игровое поле
    controls = [s for s in slots + cards]
    page.add(ft.Stack(controls=controls, width=2000, height=500))
    logger.debug('Игровая зона добавлена')


if __name__ == '__main__':
    logger.info('RUN PROJECT')
    ft.app(target=main)
    # ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
