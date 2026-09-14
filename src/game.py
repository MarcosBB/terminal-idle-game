import json
import os

from src.configs import (
    DEFAULT_MONEY,
    DEFAULT_PROPERTIES,
    MULTIPLIER_OPTIONS,
    MAX_VALUE,
    SAVE_FILE_PATH,
    SECONDS_PER_FRAME,
)


class Game:
    def __init__(
        self,
        properties=DEFAULT_PROPERTIES,
        money=DEFAULT_MONEY,
        multiplier_options=MULTIPLIER_OPTIONS,
        save_file_path=SAVE_FILE_PATH,
    ):
        self.money = money
        self.properties = properties
        self.multiplier_index = 0
        self.multiplier_options = multiplier_options
        self.save_file_path = save_file_path
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
        data = {
            "money": self.money,
            "multiplier_index": self.multiplier_index,
            "properties": {
                property["name"]: property["quantity"] for property in self.properties
            },
        }
        with open(self.save_file_path, "w") as save_file:
            json.dump(data, save_file)

    def load(self):
        if not os.path.exists(self.save_file_path):
            return

        with open(self.save_file_path, "r") as save_file:
            try:
                data = json.load(save_file)
            except json.JSONDecodeError:
                return

        self.money = data.get("money", self.money)
        self.multiplier_index = data.get("multiplier_index", self.multiplier_index)

        saved_quantities = data.get("properties", {})
        for property in self.properties:
            property["quantity"] = saved_quantities.get(
                property["name"], property["quantity"]
            )

        self.update_money_per_second()
        self.update_money_per_second_by_property()
