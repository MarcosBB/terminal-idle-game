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
    ):
        self.money = money
        self.properties = properties
        self.money_per_second = self.update_money_per_second()
        self.multiplier_index = 0

    def earn_money(self):
        for property in self.properties:
            self.money += property["quantity"] * property["income"] * SECONDS_PER_FRAME

    def buy_property(self, index, quantity=1):
        if self.get_multiplier == MAX_VALUE:
            possible_quantity = self.money // self.properties[index]["value"]
            self.money -= possible_quantity * self.properties[index]["value"]
            self.properties[index]["quantity"] += possible_quantity

        elif self.money >= self.properties[index]["value"] * self.get_multiplier:
            self.money -= self.properties[index]["value"] * self.get_multiplier
            self.properties[index]["quantity"] += quantity * self.get_multiplier

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
        multiplier_len = len(MULTIPLIER_OPTIONS)
        self.multiplier_index += 1
        if self.multiplier_index >= multiplier_len:
            self.multiplier_index = 0

    @property
    def get_multiplier(self):
        return MULTIPLIER_OPTIONS[self.multiplier_index]

    def save(self):
        pass
