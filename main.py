from game import Game
from menu import Menu
import time
import os
from configs import PROPERTIES
from pynput import keyboard

game = Game()
menu = Menu(game)


def on_press(key):
    for i in range(1, len(PROPERTIES) + 1):
        if key == keyboard.KeyCode.from_char(str(i)):
            game.buy_property(PROPERTIES[i-1], 1)
            game.update_money_per_second()
            game.update_money_per_second_by_property()

    if key == keyboard.KeyCode.from_char("x"):
        game.change_multiplier()

    if key == keyboard.KeyCode.from_char("s"):
        game.save()


with keyboard.Listener(on_press=on_press) as listener:
    while True:
        game.earn_money()
        menu.print_menu()
        time.sleep(1)
        os.system('clear')

