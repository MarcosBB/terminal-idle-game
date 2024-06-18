from src.configs import (
    DEFAULT_MONEY,
    DEFAULT_PROPERTIES,
    PROPERTIES_INCOME,
    PROPERTIES_VALUES,
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
        self.money_per_second_by_property = self.update_money_per_second_by_property()
        self.multiplier_index = 0

    def earn_money(self):
        for key in self.properties:
            self.money += self.properties[key] * PROPERTIES_INCOME[key] * SECONDS_PER_FRAME

    def buy_property(self, property_name, quantity=1):
        if self.get_multiplier == MAX_VALUE:
            possible_quantity = self.money // PROPERTIES_VALUES[property_name]
            self.money -= possible_quantity * PROPERTIES_VALUES[property_name]
            self.properties[property_name] += possible_quantity

        elif self.money >= PROPERTIES_VALUES[property_name] * self.get_multiplier:
            self.money -= PROPERTIES_VALUES[property_name] * self.get_multiplier
            self.properties[property_name] += quantity * self.get_multiplier

    def update_money_per_second(self):
        self.money_per_second = 0
        for key in self.properties:
            self.money_per_second += self.properties[key] * PROPERTIES_INCOME[key]
        return self.money_per_second

    def update_money_per_second_by_property(self):
        self.money_per_second_by_property = {}
        for key in self.properties:
            self.money_per_second_by_property[key] = (
                self.properties[key] * PROPERTIES_INCOME[key]
            )
        return self.money_per_second_by_property

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
