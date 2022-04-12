class Card:
    def __init__(self, dicto):
        self.name = dicto["name"]
        self.__dict__["card type"] = dicto["type"]
        self.effect = dicto["desc"]
        self.type = dicto["race"]

    def __bool__(self):
        return True

    def __str__(self):
        def no_name_effect():
            liste = []
            for attribute in self.__dict__:
                if attribute in ["name", "effect"]:
                    continue
                liste.append(str(self[attribute]))
            return "   ".join(liste)
        return f'{self.name}\n{no_name_effect()}\n{self.effect}'

    def __getitem__(self, key):
        return self.__dict__[key]

class Monster(Card):
    def __init__(self, dicto):
        super().__init__(dicto)
        self.type = dicto["race"]
        self.attribute = dicto["attribute"].title()
        self.level = dicto["level"]
        self.atk = dicto["atk"]
        self.__dict__["def"] = dicto["def"]

class Spell(Card):
    def __bool__(self):
        if self.type == "Ritual":
            return False
        elif self.name in ["Super Polymerization", "Polymerization"]:
            return False
        return super().__bool__()

class Trap(Card):
    pass
