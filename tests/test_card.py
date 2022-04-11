from requests import get

from .classe.card import Card

print(get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php"))


class Test_card:
    def test_init(self):
        tempo = Card({"allo":3})
        raise NotImplementedError("Test to check the init of a single card!")