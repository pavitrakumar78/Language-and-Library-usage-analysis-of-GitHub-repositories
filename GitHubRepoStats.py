# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 11:49:40 2017

@author: Pavitrakumar
"""

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas import DataFrame
import matplotlib.pyplot as plt
import time
import datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

def make_url(base_url, search_params, query_params):
    url = base_url
    query = ""
    query_chunks = []
    for param, value in query_params.items():
        if param is '':
            query_chunks.append(value)
        else:
            query_chunks.append("%s:%s" % (param, value))
    #print(query_chunks)
    query = ' '.join(query_chunks)
    search_params['q'] = query
    if search_params:
        url = '{}?{}'.format(url, urllib.parse.urlencode(search_params))
    #print(url)
    return url



def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def gen_dates(created_from, created_till, intreval = "month"):
    from_date = datetime.datetime.strptime(created_from, "%Y-%m-%d")
    to_date = datetime.datetime.strptime(created_till, "%Y-%m-%d") 
    today = datetime.datetime.today()
    
    if (today - to_date).days < 0:
        to_date = today
    
    diff = diff_month(to_date, from_date)

    if intreval == "year":
        if diff < 12:
            print("Less than 1 year difference between 2 dates; Cannot generate yearly statistics")
            return
        else:
            diff = int(diff/12)
            add_to_date = relativedelta(years=1)
    elif intreval == "month":
        add_to_date = relativedelta(months=1)    
        
    date_pairs = []
    
    curr_date = from_date
    
    for i in range(diff):
        future_date = curr_date + add_to_date
        date_pairs.append((curr_date.strftime("%Y-%m-%d"),future_date.strftime("%Y-%m-%d")))
        curr_date = future_date
    
    return date_pairs
    
def get_statistics(search_string, search_language, created_from, created_till, intreval = "month"):
    search_params = {'type' : 'repositories'}
    #search_params = {'o' : 'asc', 's' : 'updated', 'type' : search_type}
    query_params = {'' : search_string, 'in' : 'file' , 'created':'', 'language':search_language}
    base_url = "https://github.com/search"
    
    date_pairs = gen_dates(created_from, created_till, intreval = intreval)
    lang_stats = []
    all_langs = set()
    
    for pair in tqdm(date_pairs):
        created_format = '{}..{}'.format(pair[0], pair[1])
        query_params['created'] = created_format
        search_url = make_url(base_url, search_params, query_params)
        #print(search_url)
        
        text = urlopen(search_url).read()
        time.sleep(6) #to avoid HTTPError: Too Many Requests| according to GitHub API docs, we can do 10 requests per min| 1 every 6 secs.
        #This limit can be increased if we use github's API but API does not allow general searching without mentioning user or repo name
        soup = BeautifulSoup(text, "lxml")
        
        #divs = soup.findAll("div", { "class" : "col-8 pr-3" }) #list of repos in the first page
        
        html_type_counts = soup.findAll("ul", { "class" : "filter-list small" })
        if len(html_type_counts) == 0:
            print("No results found for given search query during dates %s and %s" % (pair[0], pair[1]))
            continue
        type_counts =  html_type_counts[0].get_text().replace(' ','').split('\n')
        type_counts = [x for x in type_counts if x is not '']
        
        lang_count_pairs = []
        
        for i in range(0,len(type_counts),2):
            lang_count_pairs.append((type_counts[i], type_counts[i+1], pair[1]))
            all_langs.add(type_counts[i+1])
        
        #print("From: %s to %s." % (pair[0],pair[1]))
        #print(lang_count_pairs)
        lang_stats.append(lang_count_pairs)
    
    #construct pandas dataframe for plotting
    #rows - date
    #cols - language
        
    all_dates = [x[1] for x in date_pairs] #these are the rows
    
    df = DataFrame(columns = all_langs,index = all_dates)
    
    for lang_count_pairs in lang_stats:
        for pair in lang_count_pairs:
            df[pair[1]][pair[2]] = int(pair[0].replace(',','')) #we use replace to take care of cases like: '1,827'
    
    df = df.fillna(0)
    return df

def plot_stats(stats,top_x):
    total_repo_count = list(stats.sum(axis=0))
    language = list(stats.columns)
    
    combined = list(zip(language, total_repo_count))
    combined.sort(key = lambda k: -k[1]) #do sorting + reverse
    
    selected_languages = [pair[0] for pair in combined[0:top_x]]
    
    f = plt.figure()
    plt.title('Language usage graph for keyword:'+search_string, color='black')
    #stats.loc[:,selected_languages].plot(kind='bar', ax=f.gca(),rot=45)
    #https://stackoverflow.com/questions/11927715/how-to-give-a-pandas-matplotlib-bar-graph-custom-colors
    stats.loc[:,selected_languages].plot(ax=f.gca(), rot=45)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.xlabel('Timeline')
    plt.ylabel('No. of repositories created')
    plt.show()


#search_type = "repositories" 
search_language = "lua"
created_from = "2016-02-01" #YYYY-MM-DD
created_till = "2017-04-01"
search_string = "torch"
intreval = "month" #"month" or "year" - display/generate statistics yearly or monthly
#plot only top x languages/technologies  
top_x = 5

stats = get_statistics(search_string, search_language, created_from, created_till, intreval)

plot_stats(stats,top_x)


