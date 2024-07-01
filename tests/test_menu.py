from unittest import TestCase
from src.menu import Menu
from src.game import Game
from src.configs import MULTIPLIER_OPTIONS, MAX_VALUE, SECONDS_PER_FRAME
from unittest.mock import patch


class MenuTestCase(TestCase):
    def setUp(self):
        self.properties = [
            {
                "name": "farmer",
                "value": 100,
                "income": 10,
                "quantity": 1,
                "money_per_second": 10,
            },
            {
                "name": "cow",
                "value": 200,
                "income": 20,
                "quantity": 0,
                "money_per_second": 0,
            },
        ]
        self.game = Game(
            properties=self.properties,
            money=1000,
        )
        self.menu = Menu(self.game)

    # def test_it_should_be_initialized_correctly(self):
    #     self.assertEqual(self.menu.game, self.game)
    #     self.assertEqual(self.menu.header, "")
    #     self.assertEqual(self.menu.properties_rich_table, "")

    def test_it_should_update_footer_correctly(self):
        self.menu.update_footer()
        self.assertEqual(
            self.menu.footer,
            "(1-2) Buy property | (x) Change buy modifier | (s) Save | (ctrl + c) Exit",
        )

    def test_it_should_update_header_correctly(self):
        self.menu.update_header()
        self.assertEqual(
            self.menu.header,
            "Money: [bold green]1K$[/bold green] | Money per second: [green]10[/green]$ | Multiplier: [blue]1X[/blue]",
        )

    def test_it_should_update_header_correctly_with_max_value(self):
        self.game.multiplier_index = MULTIPLIER_OPTIONS.index(MAX_VALUE)
        self.menu.update_header()
        self.assertEqual(
            self.menu.header,
            "Money: [bold green]1K$[/bold green] | Money per second: [green]10[/green]$ | Multiplier: [blue]Max[/blue]",
        )

    def test_it_should_update_properties_rich_table(self):
        self.menu.properties_table = None
        self.menu.update_properties_rich_table()
        self.assertIsNotNone(self.menu.properties_table)

    def test_it_should_update_properties_table(self):
        self.menu.properties_table = None
        self.menu.update_properties_table()
        self.assertIsNotNone(self.menu.properties_table)
