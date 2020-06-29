def searchg(query):
   from googleapiclient.discovery import build
   import json
   import rankaggregation as ra
   import requests
   from collections import OrderedDict
   import nltk
   nltk.download('stopwords')
   nltk.download('punkt')

   # Google Search
   my_api_key = '''AIzaSyBQP64b5yAKUdj8StHtEMy2VnkJzizIXIw'''
   my_cse_id = '''016035045891452815853:spx1m4krseb'''

   def google_search(search_term, api_key, cse_id, **kwargs):
      service = build("customsearch", "v1", developerKey=api_key)
      res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
      return res['items']

   results = google_search(query, my_api_key, my_cse_id)

   google_title = []
   google_link = []
   for result in results:
      # print(result.get('title'))
      google_title.append(result.get('title'))
      # print(result.get('link'))
      google_link.append(result.get('link'))
      # print(result.get('snippet'))
      # print('\n')
   # google_dictionary = OrderedDict()
   google_dictionary = OrderedDict(zip(google_link, google_title))

   # Bing Search
   subscription_key = '''71ba2bbf7fa14df386d0f505cb03ba0a'''
   assert subscription_key

   def bing_search(query):
      search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
      search_term = query
      headers = {"Ocp-Apim-Subscription-Key": subscription_key}
      params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
      response = requests.get(search_url, headers=headers, params=params)
      response.raise_for_status()
      search_results = response.json()
      return search_results

   results = bing_search(query)
   print(type(results))
   bing_title = []
   bing_link = []

   for v in results["webPages"]["value"]:
      # print("   url: ",  v["url"])
      bing_link.append(v["url"])
      # print("   Name:",v["name"])
      bing_title.append(v["name"])
      # print("   Snippet:", v["snippet"])
      # print('\n')
   # bing_dictionary = OrderedDict()


   bing_dictionary = OrderedDict(zip(bing_link, bing_title))
   # rankAggregration
   agg = ra.RankAggregator()
   collected_links = []
   collected_title = []
   treemap_links = [google_link, bing_link]
   collected_links = [i[0] for i in agg.borda(treemap_links)]
   print(collected_links)
   for url in collected_links:
      if url in google_dictionary.keys():
         collected_title.append(google_dictionary[url])
      else:
         collected_title.append(bing_dictionary[url])

   collected_dictionary = OrderedDict()
   collected_dictionary = OrderedDict(zip(collected_title, collected_links))
   output_dict = json.loads(json.dumps(collected_dictionary))
   return output_dict


from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      k=result.get("Name")

      # print(k)

      dict = searchg(k)
      # print(dict)
      # call the function here and pass k as query
      # that function will return a dictionary containing topic name and link related to that.
      # dict = {0: 'http://www.google.com',1: 'https://www.geeksforgeeks.org/', 2: 'https://www.tutuapp.vip/pc/'}
      # dict = {'phy': 50, 'che': 60, 'maths': 70}
      # dict = {'Topic 1': {'Google': 'http://www.google.com', 'GeeksforGeeks': 'https://www.geeksforgeeks.org/' }, 'Topic 2': {'tutu': 'https://www.tutuapp.vip/pc/', 'age': '25'}}
      return render_template("result.html",result = dict)

if __name__ == '__main__':
   app.run(debug = True)


