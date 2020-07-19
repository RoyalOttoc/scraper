import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://au.indeed.com/jobs?q=python&limit={LIMIT}&radius=25"


def extract_indeed_pages():

    indeed_result = requests.get(URL)

    soup = BeautifulSoup(indeed_result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})

    if company is None:
        company = ("No Company Name")
    else:
        if company.find("a") is not None:
            company = company.find("a").string
        else:
            company = company.string
            company = company.strip()
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {"title": title, "company": company, "location": location, "link": f"https://au.indeed.com/viewjob?jk={job_id}"}


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
      print(f"scrapping page {page}")
      result = requests.get(f"{URL}&start={page*LIMIT}")
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
      for result in results:
          job = extract_job(result)
          jobs.append(job)
    return jobs

def get_jobs():
  last_indeed_page  = extract_indeed_pages()
  jobs = extract_indeed_jobs(last_indeed_page)
  return jobs