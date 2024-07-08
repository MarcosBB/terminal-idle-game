from unittest import TestCase
from src.game import Game
from src.configs import MULTIPLIER_OPTIONS, MAX_VALUE, SECONDS_PER_FRAME
from parameterized import parameterized


class GameTestCase(TestCase):

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
            multiplier_options=[1, 5, 500, MAX_VALUE],
        )

    def test_it_should_be_initialized_correctly(self):
        self.assertEqual(self.game.money, 1000)
        self.assertEqual(self.game.properties, self.properties)
        self.assertEqual(self.game.multiplier_index, 0)
        self.assertEqual(self.game.money_per_second, 10)

    @parameterized.expand(
        [
            (1000, 0, 2, 900),
            (1000, 1, 6, 500),
            (1000, 2, 1, 1000),
            (1000, 3, 11, 0),
            (20, 1, 1, 20),
            (999, 3, 10, 99),
        ]
    )
    def test_it_should_buy_property_correctly(
        self, money, multiplier_index, expected_quantity, expected_money
    ):
        self.game.money = money
        self.game.multiplier_index = multiplier_index
        self.game.buy_property(index=0)
        self.assertEqual(self.game.properties[0]["quantity"], expected_quantity)
        self.assertEqual(self.game.money, expected_money)

    @parameterized.expand([
        (0, 1),
        (3, 0),
        (7, 0),
    ])
    def test_it_should_change_multiplier_correctly(self, multiplier_index, expected_index):
        self.game.multiplier_index = multiplier_index
        self.game.change_multiplier()
        self.assertEqual(self.game.multiplier_index, expected_index)

    def test_it_should_change_multiplier_correctly_when_it_is_max_value(self):
        self.game.multiplier_index = len(MULTIPLIER_OPTIONS) - 1
        self.game.change_multiplier()
        self.assertEqual(self.game.multiplier_index, 0)

    def test_it_should_update_money_per_second_correctly(self):
        self.game.update_money_per_second()
        self.assertEqual(self.game.money_per_second, 10)

    def test_it_should_update_money_per_second_by_property_correctly(self):
        self.game.properties[0]["quantity"] = 2
        self.game.properties[1]["quantity"] = 1
        self.game.update_money_per_second_by_property()
        self.assertEqual(self.game.properties[0]["money_per_second"], 20)
        self.assertEqual(self.game.properties[1]["money_per_second"], 20)

    def test_it_should_earn_money_correctly(self):
        self.game.earn_money()
        self.assertEqual(self.game.money, 1000 + 10 * SECONDS_PER_FRAME)

    def test_it_should_get_multiplier_correctly(self):
        self.assertEqual(self.game.get_multiplier, MULTIPLIER_OPTIONS[0])
