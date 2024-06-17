from configs import DEFAULT_PROPERTIES, PROPERTIES_INCOME


class Menu():
    def __init__(self, game):
        self.game = game

    def header(self):
        return f"Money: {self.game.money}$ | Money per second: {self.game.money_per_second}$ | Multiplier: {self.game.get_multiplier}X"
    
    def footer(self):
        return f"(1-{len(DEFAULT_PROPERTIES)}) Buy property | (x) Change buy modifier | (s) Save | (ctrl + c) Exit" 

    def properties(self):
        return_value = ""
        count = 0
        for key, value in self.game.properties.items():
            count += 1
            if value != 0:
                return_value += f"{count}. {key}: {value}    {value * PROPERTIES_INCOME[key]} /s\n"
            else:
                return_value += f"{count}. {key}: {value}\n"
        return return_value
    

    def print_menu(self):
        print(self.header())
        print(self.properties())
        print(self.footer())