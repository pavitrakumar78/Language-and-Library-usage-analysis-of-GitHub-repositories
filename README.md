# Language and Library usage analysis of GitHub repositories.

A simple script to visualize the number of GitHub repositories created in a timeline for a given keyword and programming language. The primary idea is to get some statistics about the usage of libraries across different languages.

## How it works  
I construct a GitHub search link using the input params given by user and extract necessary contents from the html of the page using BeautifulSoup. Multiple searches are made depending on the timeline params (monthly or yearly). My intension was to find the usage of same libraries in different langauges (demonstrated in the example 1). But since the search performs exactly like the search bar in GitHub, we can also use it to search for function names, repo names etc.,

Note: I do not think general search (without mentioning repository name or username) is possible using GitHub's API, so that is why I have used raw crawling. If you try searching without mentioning anything (like we do in the search bar) you will get [this](https://api.github.com/search/code?q=addClass+in:file+language:js). Also, another downside is that using this script, you cannot request more than 10 requests per minute (`sleep` has been added in this script to allow more requests, but long timelines will take more time).

## Example 1:
 
```python
search_language = "lua"
created_from = "2016-02-01" #YYYY-MM-DD
created_till = "2017-04-01"
search_string = "torch"
intreval = "month" #"month" or "year" - display/generate statistics yearly or monthly
#plot only top x languages  
top_x = 5

stats = get_statistics(search_string, search_language, created_from, created_till)

plot_stats(stats,top_x)
```

### Output:  

<img src="https://github.com/pavitrakumar78/Language-and-Library-usage-analysis-of-GitHub-repositories/blob/master/sample.png" />  


## Example 2:

```python
search_language = "python"
created_from = "2013-02-01" #YYYY-MM-DD
created_till = "2017-04-01"
search_string = "deep learning"
intreval = "year" #"month" or "year" - display/generate statistics yearly or monthly
#plot only top x languages/technologies  
top_x = 7

stats = get_statistics(search_string, search_language, created_from, created_till)

plot_stats(stats,top_x)
```
### Output:  

<img src="https://github.com/pavitrakumar78/Language-and-Library-usage-analysis-of-GitHub-repositories/blob/master/sample2.png" />  

## Dependencies:
Python 3.5  

### Libraries:  
urllib  
BeautifulSoup  
pandas  
matplotlib  
tqdm  
