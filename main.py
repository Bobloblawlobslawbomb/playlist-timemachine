from bs4 import BeautifulSoup
import requests


user_date = input(
    "What date would you lke the top 100 songs for? (YYYY-MM-DD): ")

response = requests.get("https://billboard.com/charts/hot-100/" + user_date)

soup = BeautifulSoup(response.text, "html.parser")

titles_list = [title.getText().strip("\n")
               for title in soup.select("li h3")][:100]

print(titles_list)
