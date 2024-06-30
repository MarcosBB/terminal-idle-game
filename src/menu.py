from src.configs import DEFAULT_PROPERTIES, MAX_VALUE
from numerize.numerize import numerize
from rich import print
from rich.table import Table


class Menu:
    def __init__(self, game):
        self.game = game
        self.update_properties_rich_table()
        self.update_footer()
        self.update_header()

    def update_header(self):
        multiplier_symbol = "X" if MAX_VALUE != self.game.get_multiplier else ""
        self.header = (
            f"Money: [bold green]{numerize(round(self.game.money))}$[/bold green] "
            + f"| Money per second: [green]{numerize(self.game.money_per_second)}[/green]$ "
            + f"| Multiplier: [blue]{str(self.game.get_multiplier) + multiplier_symbol}[/blue]"
        )

    def update_footer(self):
        self.footer = f"(1-{len(DEFAULT_PROPERTIES)}) Buy property | (x) Change buy modifier | (s) Save | (ctrl + c) Exit"
    
    def update_properties_rich_table(self):
        table = Table(title="", box=None)
        table.add_column("Buy Option", justify="right", style="white")
        table.add_column("Value", justify="left", style="white")
        table.add_column("Property", justify="left", style="blue")
        table.add_column("Quantity", justify="right", style="purple")
        table.add_column("Money/s", justify="right", style="green")

        count = 0
        for property in self.game.properties:
            count += 1
            table.add_row(
                str(count),
                f"{property["value"]}$",
                property["name"].capitalize(),
                numerize(property["quantity"]),
                f"{numerize(property["money_per_second"])}$",
            )
        self.properties_table = table

    def update_properties_table(self):
        return_value = ""
        count = 0
        for property in self.game.properties:
            count += 1
            if property["quantity"] != 0:
                return_value += f"{count}. {property["name"]}: {numerize(property["quantity"])}    {numerize(property["money_per_second"])} /s\n"
            else:
                return_value += f"{count}. {property["name"]}: {property["quantity"]}\n"
        self.properties_table = return_value
    
    def print_menu(self):
        print(self.header)
        print()
        print(self.properties_table)
        print()
        print(self.footer)
