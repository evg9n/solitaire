# Логгер
# from loguru import logger
import flet as ft

from solitaire import Solitaier
from constants import logger


def main(page: ft.Page):
    solitaire = Solitaier()
    page.add(solitaire)


if __name__ == '__main__':
    # logger.info('RUN PROJECT')
    # ft.app(target=main, view=ft.WEB_BROWSER)
    ft.app(target=main)
