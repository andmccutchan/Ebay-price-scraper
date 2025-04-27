from bs4 import BeautifulSoup
import requests

query = input("What would you like to search for? ").replace(" ", "+")

url = f"https://www.ebay.com/sch/i.html?_nkw={query}&_sacat=0&_from=R40&_trksid=p4432023.m570.l1311"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
items = doc.find(class_="srp-river-results")

prices = items.find_all("span", class_="s-item__price")
descriptions = items.find_all("div", class_="s-item__title")

item_description_with_price = []

for price, description in zip(prices, descriptions):
    price_number = price.text.replace("$", "").replace(",", "")
    if " to " in price_number:
        price_range = price_number.replace(" to ", " ").split()
        price_float = float(price_range[0])
        item_description_with_price.append((price_float, description.text))
    else:
        price_float = float(price_number)
        item_description_with_price.append((price_float, description.text))
    
    
item_description_with_price.sort()

with open("output.txt", "w") as file:
    for i, (price, description) in enumerate(item_description_with_price, 1):
        file.write(f"{i} -- {description} -- ${price}\n")
    

