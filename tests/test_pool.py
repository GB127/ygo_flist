from copy import copy
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

    def test_discard(self):
        copie_card = copy(Test_pool.classe.pool[0])
        Test_pool.classe.take_discard([copie_card])
        assert len(Test_pool.classe.discard) == 1
        assert len(Test_pool.classe.pool) == 4  # 4 because one card was dealt in a previous test.


    def test_mix_discard_pool(self):
        Test_pool.classe.mix_discarded_pool()
        assert len(Test_pool.classe.pool) == 5