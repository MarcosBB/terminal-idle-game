import json
import os
import tempfile
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
        self.save_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.save_file.close()
        os.remove(self.save_file.name)
        self.game = Game(
            properties=self.properties,
            money=1000,
            multiplier_options=[1, 5, 500, MAX_VALUE],
            save_file_path=self.save_file.name,
        )

    def tearDown(self):
        if os.path.exists(self.save_file.name):
            os.remove(self.save_file.name)

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

    @parameterized.expand(
        [
            (0, 1),
            (3, 0),
            (7, 0),
        ]
    )
    def test_it_should_change_multiplier_correctly(
        self, multiplier_index, expected_index
    ):
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

    def test_it_should_save_game_correctly(self):
        self.game.money = 1500
        self.game.multiplier_index = 2
        self.game.properties[0]["quantity"] = 3
        self.game.properties[1]["quantity"] = 1

        self.game.save()

        with open(self.save_file.name) as save_file:
            data = json.load(save_file)

        self.assertEqual(
            data,
            {
                "money": 1500,
                "multiplier_index": 2,
                "properties": {"farmer": 3, "cow": 1},
            },
        )

    def test_it_should_load_game_correctly(self):
        with open(self.save_file.name, "w") as save_file:
            json.dump(
                {
                    "money": 2500,
                    "multiplier_index": 1,
                    "properties": {"farmer": 4, "cow": 2},
                },
                save_file,
            )

        self.game.load()

        self.assertEqual(self.game.money, 2500)
        self.assertEqual(self.game.multiplier_index, 1)
        self.assertEqual(self.game.properties[0]["quantity"], 4)
        self.assertEqual(self.game.properties[1]["quantity"], 2)
        self.assertEqual(self.game.money_per_second, 4 * 10 + 2 * 20)
        self.assertEqual(self.game.properties[0]["money_per_second"], 4 * 10)
        self.assertEqual(self.game.properties[1]["money_per_second"], 2 * 20)

    def test_it_should_do_nothing_when_loading_without_a_save_file(self):
        self.game.load()

        self.assertEqual(self.game.money, 1000)
        self.assertEqual(self.game.multiplier_index, 0)
        self.assertEqual(self.game.properties, self.properties)

    def test_it_should_do_nothing_when_loading_a_corrupted_save_file(self):
        with open(self.save_file.name, "w") as save_file:
            save_file.write("not valid json")

        self.game.load()

        self.assertEqual(self.game.money, 1000)
        self.assertEqual(self.game.multiplier_index, 0)
        self.assertEqual(self.game.properties, self.properties)

    def test_it_should_ignore_unknown_properties_when_loading(self):
        with open(self.save_file.name, "w") as save_file:
            json.dump(
                {
                    "money": 500,
                    "multiplier_index": 0,
                    "properties": {"farmer": 2, "dragon": 99},
                },
                save_file,
            )

        self.game.load()

        self.assertEqual(self.game.properties[0]["quantity"], 2)
        self.assertEqual(self.game.properties[1]["quantity"], 0)
