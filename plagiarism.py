import requests
import re
import urllib.parse
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Online_Plagiarism:
  def googleSearch(self, query):
    g_clean = [ ]
    len = 0
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
    try:
      html = requests.get(url)
      if html.status_code==200:
        soup = BeautifulSoup(html.text, 'lxml')
        a = soup.find_all('a')
        for i in a:
          k = i.get('href')
          try:
            m = re.search("(?P<url>https?://[^\s]+)", k)
            n = m.group(0)
            rul = n.split('&')[0]
            domain = urlparse(rul)
            if(re.search('google.com', domain.netloc)):
              continue
            else:
              g_clean.append(rul)
              len += 1
              if (len == 3):
                return g_clean
          except:
            continue
    except Exception as ex:
          print(str(ex))
    finally:
          return g_clean

  def check_text(self, text_query):
    out= []
    text_final = []
    obj = Offline_Plagiarism()
    text = text_query
    temp = text.split('.')
    try:
      for i in range(0, len(temp), 3):
        text_final.append(temp[i]+'. '+temp[i+1]+'. '+temp[i+2])
    except:
      text_final.append('.'.join(temp[i:]))
    for query in text_final:
      results = set ()
      for i in query.split('.'):
        if (i != ''):
          results.update(self.googleSearch(i)[:3])
      header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
      responses = list(map(lambda x: [x,requests.request('GET', x ,headers = header, verify = False).text], results))
      for i in responses:
        TAG_RE = re.compile(r'<[^>]+>')
        clean_1 = TAG_RE.sub('', i[1])
        second = re.compile(r'&.*?;')
        cleantext = second.sub('',clean_1)
        final = re.sub('[^A-Za-z0-9]+', ' ', cleantext)
        query = re.sub('[^A-Za-z0-9.]+', ' ', query)
        val = obj.check_text(final.lower(), query.lower())
        for j in query.split('.'):
          if re.search(j.lower(), final.lower()):
            out.append([i[0],query,val[:val.index('%')]])
            break
    return out

class Offline_Plagiarism:
  def check_text(self, input1,input2):
    to_check = []
    text = input1
    to_check.append(text)
    text = input2
    to_check.append(text)
    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
    vectors = vectorize(to_check)
    s_vectors = list(zip(['First Text','Second Text'], vectors))
    return str("{:.2f}".format(self.check_plagiarism(s_vectors)*100))+'% Similarity Found'
  
  def check_plagiarism(self, s_vectors):
      sim_score = None
      similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
      for student_a, text_vector_a in s_vectors:
          new_vectors =s_vectors.copy()
          current_index = new_vectors.index((student_a, text_vector_a))
          del new_vectors[current_index]
          for student_b , text_vector_b in new_vectors:
              sim_score = similarity(text_vector_a, text_vector_b)[0][1]
      return sim_score