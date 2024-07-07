from src.configs import (
    DEFAULT_MONEY,
    DEFAULT_PROPERTIES,
    MULTIPLIER_OPTIONS,
    MAX_VALUE,
    SECONDS_PER_FRAME,
)


class Game:
    def __init__(
        self,
        properties=DEFAULT_PROPERTIES,
        money=DEFAULT_MONEY,
        multiplier_options=MULTIPLIER_OPTIONS,

    ):
        self.money = money
        self.properties = properties
        self.multiplier_index = 0
        self.multiplier_options = multiplier_options
        self.money_per_second = self.update_money_per_second()

    def earn_money(self):
        for property in self.properties:
            self.money += property["quantity"] * property["income"] * SECONDS_PER_FRAME

    def buy_property(self, index):
        if self.get_multiplier == MAX_VALUE:
            quantity = self.money // self.properties[index]["value"]
        else:
            quantity = self.get_multiplier

        if quantity and self.money >= self.properties[index]["value"] * quantity:
            self.money -= self.properties[index]["value"] * quantity
            self.properties[index]["quantity"] += quantity

    def update_money_per_second(self):
        self.money_per_second = 0
        for property in self.properties:
            self.money_per_second += property["quantity"] * property["income"]
        return self.money_per_second

    def update_money_per_second_by_property(self):
        self.money_per_second_by_property = {}
        for property in self.properties:
            property["money_per_second"] = property["quantity"] * property["income"]

    def change_multiplier(self):
        multiplier_len = len(self.multiplier_options)
        self.multiplier_index += 1
        if self.multiplier_index >= multiplier_len:
            self.multiplier_index = 0

    @property
    def get_multiplier(self):
        return self.multiplier_options[self.multiplier_index]

    def save(self):
        pass
