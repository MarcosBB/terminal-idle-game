from unittest import TestCase
from src.game import Game

class GameTestCase(TestCase):
    def setUp(self):
        self.game = Game()
        self.game.money = 1000

    def test_user_should_buy_property(self):
        pass
    #     self.game.buy_property(1)

    #     self.assertEqual(self.game.properties["property1"], 2)

    #     self.assertEqual(self.game.money, 900)

        

