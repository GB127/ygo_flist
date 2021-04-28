import requests


def ban_later():
    end = "10/26/2010"
    today = "04/27/2021"
    rep_toban = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?&startdate={end}&enddate={today}&dateregion=tcg_date")
    if rep_toban.status_code == 200:
        all_toban = rep_toban.json()["data"]
    else:
        raise BaseException("Something went wrong")
    toreturn = ""
    for card in all_toban:
        toreturn += f"{card['id']} 0 \n"
    return toreturn

def get_cards_pool():
    end = "10/26/2010"
    start = "02/04/1999"
    rep = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?&startdate={start}&enddate={end}&dateregion=tcg_date")
    if rep.status_code == 200:
        card_pool = rep.json()["data"]
    else:
        raise BaseException("Something went wrong")
    return card_pool

if __name__ == "__main__":
    towrite = ""
    towrite += ban_later()



