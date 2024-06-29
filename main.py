from src.game import Game
from src.menu import Menu
import time
import os
from src.configs import PROPERTIES, SECONDS_PER_FRAME
from pynput import keyboard

game = Game()
menu = Menu(game)


def on_press(key):
    for i in range(1, len(PROPERTIES) + 1):
        if key == keyboard.KeyCode.from_char(str(i)):
            game.buy_property(PROPERTIES[i - 1], 1)
            game.update_money_per_second()
            game.update_money_per_second_by_property()
            menu.update_properties_rich_table()

    if key == keyboard.KeyCode.from_char("x"):
        game.change_multiplier()

    if key == keyboard.KeyCode.from_char("s"):
        game.save()

with keyboard.Listener(on_press=on_press) as listener:
    frame_rate_problem = 0
    while True:
        start_time = time.time()
        os.system("clear")
        game.earn_money()
        menu.update_header()
        menu.print_menu()
        end_time = time.time()
        run_time = end_time - start_time

        if run_time < SECONDS_PER_FRAME:
            if frame_rate_problem > 10:
                print(f"WARNING: Frame rate problem detected {frame_rate_problem} times!")
            time.sleep(SECONDS_PER_FRAME - run_time)
        else:
            frame_rate_problem += 1
        
        
