import requests
from bs4 import BeautifulSoup

page= 1
URL = f"https://www.seek.com.au/python-jobs?page={page}"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("p", {"class": "_1eeNbu7"})
  links = pagination.find_all('a')

  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))

  max_page = pages[-1]
  print(max_page)
  

def get_jobs():
  last_page = get_last_page()
  
  

  