from classe.user import User
import pytest


class Test_user:
    def test_init(self):
        with pytest.raises(AssertionError):
            User("Allo")
        for name in ["Guylain", "Maxime"]:
            for attribute in ["cards", "username"]:
                assert hasattr(User(name), attribute)

    def test_take_card(self):
        test = User("Guylain")
        test.take_cards(["carte"])
        assert len(test.cards) == 1
