from configs import DEFAULT_PROPERTIES
# from pynput import keyboard
# from pick import pick


class Menu():
    def __init__(self, game):
        self.game = game

    def header(self):
        return f"Money: {self.game.money}$ | Money per second: {self.game.money_per_second}$ | Multiplier: {self.game.get_multiplier()}X"
    
    def footer(self):
        return "1 - Buy 1 property | 2 - Buy 10 properties | 3 - Save | 4 - Exit" 

    def properties(self):
        return_value = ""
        count = 0
        for key, value in self.game.properties.items():
            count += 1
            return_value += f"{count}. {key}: {value}\n"
        return return_value
    

    def print_menu(self):
        print(self.header())
        print(self.properties())
        print(self.footer())