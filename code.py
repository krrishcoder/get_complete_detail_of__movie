import requests
import re
from bs4 import BeautifulSoup
from googlesearch import search

#year of release  --> done
#duration of movie  -->done  done
#director  --> done done
#genres   --> done by just watch
#short summary --> done by justwatch

query = "Emancipation country india  /justwatch "
url = ""

my_results_list = []

for i in search(query,        # The query you want to run
                tld = 'com',  # The top level domain
                lang = 'en',  # The language
                num = 10,     # Number of results per page
                start = 0,    # First result to retrieve
                stop = None,  # Last result to retrieve
                pause = 2.0,  # Lapse between HTTP requests
               ):
    #my_results_list.append(i)
    if("https://www.justwatch.com/in/" in i):
      url  = i
      break

response = requests.get(url)

if response.status_code == 200:
    html_content = response.content
    soup = BeautifulSoup(html_content, "lxml")
    # Example: Extract all the links on the page

    div_class_b = 'text-muted'
    div_b = soup.find_all('span', class_=div_class_b)


    year = ""
    summary =""
    for div in div_b:
      year = div.get_text()

    div_class = 'title-info title-info'
    div_ = soup.find('div', class_=div_class)


    p_class = 'text-wrap-pre-line mt-0'
    p_ = soup.find('p', class_=p_class)

    summary = p_.get_text()


    genres = None
    age_rating = None

# Loop through each div to extract genres and age rating
    text = ""
    for div in div_:
      text = text + div.get_text()

   # print(text)
    pattern = r"Genres([\w\s&,]+)"
    match = re.search(pattern, text)

    runtime_pattern = r"Runtime(\d+h \d+min)"
    age_rating_pattern = r"Age rating([A-Z]+)"
    director_pattern = r"Director\s([A-Za-z\s.]+)"

    runtime_match = re.search(runtime_pattern, text)
    age_rating_match = re.search(age_rating_pattern, text)
    director_match = re.search(director_pattern, text)

    runtime = runtime_match.group(1) if runtime_match else None
    age_rating = age_rating_match.group(1) if age_rating_match else None
    director = director_match.group(1) if director_match else None








    dis_b = {}
    if match:
      genres = match.group(1).strip()
      genres_list = [genre.strip() for genre in genres.split(",")]
      arr = genres_list[:-1]
      data = genres_list[-1]

      index_of_runtime = data.find('Runtime')
      result = data[:index_of_runtime]
      arr.append(result)

      dis_b["year"] = year
      dis_b["Age rating"] = age_rating
      dis_b["run time"] = runtime
      dis_b["summary"] = summary
      dis_b["Director"] = director
      dis_b["Genres"]= arr
      dis_b["url"] = url
      print(dis_b)
    else:
      print("Genres not found.")


