import requests
from bs4 import BeautifulSoup

start_page= 1
URL = f"https://www.seek.com.au/python-jobs?page={start_page}"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("p", {"class": "_1eeNbu7"})
  links = pagination.find_all('a')

  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))

  max_page = pages[-1]
  return max_page

def extract_job(html):
    title = html.find("a", {"class": "_2iNL7wI"}).string
    company = html.find("a", {"class": "_3AMdmRg"}).string

    company = company.string
    company = company.strip()
    
    location_box = html.find("strong", {"class": "lwHBT6d"})
    location =  location_box.find("a", {"class": "_3AMdmRg"}).string
    job_id = html["data-job-id"]
    return {"title": title, "company": company, "location": location, "link": f"https://www.seek.com.au/job/{job_id}"} 

def extract_seek_jobs(last_page):
    jobs = []
    for page in range(last_page):
      print(f"scrapping page {page}")
      result = requests.get(f"https://www.seek.com.au/python-jobs?page={start_page*page}")
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("article", {"class":"_2m3Is-x _3KQ6cQG"})
      
      for result in results:
          job = extract_job(result)
          jobs.append(job)
    return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_seek_jobs(last_page)
  return jobs
  
  
