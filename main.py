from src.game import Game
from src.menu import Menu
import argparse
import time
from rich.console import Console
from rich.live import Live
from src.configs import DISPLAY_SECONDS_PER_FRAME, SECONDS_PER_FRAME
from pynput import keyboard

parser = argparse.ArgumentParser()
parser.add_argument(
    "--reset",
    action="store_true",
    help="Start a new game instead of loading the existing save",
)
args = parser.parse_args()

game = Game()
if not args.reset:
    game.load()
menu = Menu(game)
console = Console()


def on_press(key):
    for i in range(1, len(game.properties) + 1):
        if key == keyboard.KeyCode.from_char(str(i)):
            game.buy_property(index=i - 1)
            game.update_money_per_second()
            game.update_money_per_second_by_property()
            menu.update_properties_rich_table()

    if key == keyboard.KeyCode.from_char("x"):
        game.change_multiplier()

    if key == keyboard.KeyCode.from_char("s"):
        game.save()


with keyboard.Listener(on_press=on_press) as listener:
    frame_rate_problem = 0
    last_render_time = 0
    with Live(menu.render(), console=console, auto_refresh=False) as live:
        while True:
            start_time = time.time()
            game.earn_money()
            if start_time - last_render_time >= DISPLAY_SECONDS_PER_FRAME:
                menu.update_header()
                live.update(menu.render(), refresh=True)
                last_render_time = start_time
            end_time = time.time()
            run_time = end_time - start_time

            if run_time < SECONDS_PER_FRAME:
                if frame_rate_problem > 10:
                    console.print(
                        f"WARNING: Frame rate problem detected {frame_rate_problem} times!"
                    )
                time.sleep(SECONDS_PER_FRAME - run_time)
            else:
                frame_rate_problem += 1
