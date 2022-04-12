from classe.pool import Pool
from random import seed

class Test_pool:
    seed(1)
    classe = Pool(5)
    def test_pool_size(self):
        assert len(Test_pool.classe) == 5

    def test_acceptable(self):
        with open("cards_list.txt", "r") as file:
            tempo = file.read().rstrip("\n").split("\n")
        for card in Test_pool.classe:
            assert card["name"] in tempo

    def test_set_aside(self):
        assert all(card["type"] != "Ritual" for card in Test_pool.classe)
        for card in ["Polymerization", "Super Polymerization"]:
            assert card not in [card["name"] for card in Test_pool.classe]

    def test_deal(self):
        dealt = Test_pool.classe.deal(1)
        assert len(Test_pool.classe) == 4
        assert len(dealt) == 1
        assert "Rainbow Veil" not in [x.name for x in Test_pool.classe]
        assert "Rainbow Veil" in dealt[0].name
