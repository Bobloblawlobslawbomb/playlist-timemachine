from bs4 import BeautifulSoup
import requests


user_date = input(
    "What date would you lke the top 100 songs for? (YYYY-MM-DD): ")
url = "https://billboard.com/charts/hot-100/"

response = requests.get(url + user_date)

page_text = response.text
soup = BeautifulSoup(page_text, "html.parser")

title_elements = soup.select("l1 h3")
titles_list = [title.getText() for title in title_elements]

print(titles_list)
