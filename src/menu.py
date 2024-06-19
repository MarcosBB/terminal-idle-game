from src.configs import DEFAULT_PROPERTIES, PROPERTIES_INCOME, MAX_VALUE, PROPERTIES_VALUES
from numerize.numerize import numerize
from rich import print
from rich.table import Table
from rich.console import Console


class Menu:
    def __init__(self, game):
        self.game = game
        self.console = Console()

    def header(self):
        multiplier_symbol = "X" if MAX_VALUE != self.game.get_multiplier else ""
        return (
            f"Money: [bold green]{numerize(round(self.game.money))}$[/bold green] "
            + f"| Money per second: [green]{numerize(self.game.money_per_second)}[/green]$ "
            + f"| Multiplier: [blue]{str(self.game.get_multiplier) + multiplier_symbol}[/blue]"
        )

    def footer(self):
        return f"(1-{len(DEFAULT_PROPERTIES)}) Buy property | (x) Change buy modifier | (s) Save | (ctrl + c) Exit"
    
    def properties(self):
        table = Table(title="", box=None)
        table.add_column("Buy Option", justify="right", style="white")
        table.add_column("Value", justify="left", style="white")
        table.add_column("Property", justify="left", style="blue")
        table.add_column("Quantity", justify="right", style="purple")
        table.add_column("Money/s", justify="right", style="green")

        count = 0
        for property_name, property_quantity in self.game.properties.items():
            count += 1
            table.add_row(
                str(count),
                f"{PROPERTIES_VALUES[property_name]}$",
                property_name.capitalize(),
                numerize(property_quantity),
                f"{numerize(property_quantity * PROPERTIES_INCOME[property_name])}$",
            )

        return table
        
    def print_menu(self):
        print(self.header())
        self.console.print(self.properties())
        print(self.footer())
