from game import Game
from menu import Menu
import time
import os
from configs import DEFAULT_PROPERTIES
from pynput import keyboard

game = Game()
menu = Menu(game)
options = [
    "Farmer",
    "Cow",
    "Sheep",
    "Pig",
]


def on_press(key):
    keys = range(1, len(options) )

    for i in range(1, len(options) + 1):
        if key == keyboard.KeyCode.from_char(str(i)):
            game.buy_property(options[i-1], 1)

    if key == keyboard.KeyCode.from_char("x"):
        game.change_multiplier()

    if key == keyboard.KeyCode.from_char("s"):
        game.save()

    if key == keyboard.KeyCode.from_char("q"):
        exit(0)




with keyboard.Listener(on_press=on_press) as listener:
    counter = 0
    while counter < 1000:
        os.system('clear')
        game.earn_money()
        menu.print_menu()
        time.sleep(1)
        os.system('clear')
        counter += 1


    listener.join()
