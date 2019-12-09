# URLtoDict
Transforms popular web dictionaries into word lists. Made for NLP data analysis. 
Only oxfordreference available currently.

DEPENDENCIES: furl, bs4, requests, urllib

Future sites: Wiktionary

Takes 4-6 seconds per webpage.

LEARN IN 30 SECONDS: 



from URLtoDict import URLtoDict

convert = URLtoDict()

oxford_url = r"https://www.oxfordreference.com/view/10.1093/acref/9780199688975.001.0001/acref-9780199688975" # dictionary of computer 
science

convert.oxfordreference(oxford_url)



TRY WITH ANY DICTIONARY FROM OXFORDREFERENCE. 
