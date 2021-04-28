import requests

end = "10/26/2010"
start = "02/04/1999"
today = "04/27/2021"

rep = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?&startdate={start}&enddate={end}&dateregion=tcg_date")
#rep_toban = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?&startdate={end}&enddate={today}&dateregion=tcg_date")

if rep.status_code == 200:
    all_cards = rep.json()["data"]
