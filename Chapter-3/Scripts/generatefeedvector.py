# generatefeedvector.py
# Page 32 in PDF version


# See if this actually runs! Might be awkward going back and forth between different python
#   installations
# Actually conda has re and feedparser, so can use iPython
# The Python install used will be a source of recurring tension. But
#   will use iPython at work (or home) whereever possible, using
#   conda install <package name> wherever possible.
# As expected, didn't find the data where it should be. But found it here:
#   https://raw.githubusercontent.com/arthur-e/Programming-Collective-Intelligence/master/chapter3/blogdata.txt
#   https://raw.githubusercontent.com/arthur-e/Programming-Collective-Intelligence/master/chapter3/feedlist.txt
# I think this assumes that the two text files are saved in the
#   working directory.
#     feedlist.txt
#     blogdata.txt
# UPDATE: I think blogdata.txt isn't necessary for doing this;
#   feedlist.txt should be sufficient. You can use the pre-made
#   blogdata.txt file if you don't want to run the code to make
#   it yourself. It's just a matrix of the blog name, the words
#   you're interested in, and the count of the words for each
#   blog-word combination. So try to run this with feedlist
#   only, which I could copy-paste and save into a new text
#   file locally.
# UPDATE: The other issue is that I'm using iPython python 3
#   instead of non-iPython python 2, and the book is in python
#   2. So if there's a subtle difference, it might be over my
#   head. Pretty sure calling python from the command line
#   invokes python 3.
# You'd run this from the command line with something like:
#   python generatefeedvector.py, after getting to the right working
#   directory.
import feedparser
import re
import os

print(os.getcwd())
print('\n')
print(os.listdir())


# Returns title and dictionary of word counts for an RSS feed
# getwordcounts('http://battellemedia.com/index.xml')
# url = 'http://battellemedia.com/index.xml' # shouldn't work - can't access site
# url = 'http://blog.outer-court.com/rss.xml' # should work
# url = 'http://blogs.abcnews.com/theblotter/index.rdf'
def getwordcounts(url):
  # Parse the feed
  d=feedparser.parse(url)
  wc={}

  # Loop over all the entries
  for e in d.entries:
    if 'summary' in e: summary=e.summary
    else: summary=e.description
    
    # Extract a list of words
    words=getwords(e.title+' '+summary)
    for word in words:
      wc.setdefault(word,0)
      wc[word]+=1

  # My guess is that some of these blogs have been discontinued since this book
  #   was written in 2007 (9 years ago). That or work blocks my access to some of
  #   these sites.
  # Need to account for. This is super sketchy, but:
  if 'title' not in d.feed: # title has to be string for subsequent stuff to work
    d.feed['title'] = '<no title>'
  if bool(wc) == False: # Has to be dictionary. First is the 'word' that you're storing the word counts under; second is the number of times it appears. So if I can't access the blog, just saying something like '<nowords>' showed up 0 times.
    wc['<no words>'] = 0

  return(d.feed.title, wc)


def getwords(html):
  # Remove all the HTML tags
  txt=re.compile(r'<[^>]+>').sub('',html)
  # Split words by all non-alpha characters
  words=re.compile(r'[^A-Z^a-z]+').split(txt)
  # Convert to lowercase
  return([word.lower() for word in words if word!=''])


# For testing:
# feedurl = 'http://battellemedia.com/index.xml' # shouldn't work - can't access site
# feedurl = 'http://blog.outer-court.com/rss.xml' # should work
# feedurl = 'http://blogs.abcnews.com/theblotter/index.rdf'
apcount={}
wordcounts={}
counter = 0
for feedurl in open('feedlist.txt'): # file # old
  counter += 1
  title, wc = getwordcounts(feedurl)
  wordcounts[title] = wc
  for word, count in wc.items():
    apcount.setdefault(word, 0)
    if count > 1:
      apcount[word] += 1


feedlist = list(wordcounts.keys())
counter - len(feedlist) # lost 30 blogs...Yikes
wordlist=[]
for w,bc in apcount.items():
  # Don't want to include words that never show up (e.g. 'ingratiate') or that
  #   always show up (e.g. 'the', 'a'), because neither are informative.
  # Adjusting by %s, so if a word constitutes less than 10% or more than 50%
  #   of words in the blog, don't include.
  frac=float(bc)/len(feedlist)
  # feedlist isn't defined anywhere, but guessing that it's just the number of feeds we're looking at
  if frac>0.1 and frac<0.5: wordlist.append(w)


# out=file('blogdata.txt','w') # original
# File isn't anything in python 3, need alternative
#   open(<path>, 'w') # open for writing. Write over existing file with same name
#   open(<path>, 'x') # create new file, open for writing
# Primer on file writing:
#   outtest = open('testfile.txt', 'w')
#   outtest.write('Blog')
#   for i in ['word1', 'word2', 'word3']:
#     outtest.write('\n')
#     outtest.write(i)
#   outtest.close()
# Primer on file reading:
#  for i in open('feedlist.txt'): # default for open() is to open for reading
#    print(i)
# Little example of the format of the blog data matrix
# Uses 999 instead of the actual word count
#  t_list = ['a', 'b', 'c', 'd', 'e']
#  t_dict = {
#    'first' : 'a', 'second' : 'b', 'third' : 'c', 'fourth' : 'd', 'fifth' : 'e'
#  }
#  out = open('testfile.txt', 'w')
#  out.write('blog')
#  for i in t_list: out.write('\t%s' % i)
#  out.write('\n')
#  for b, w in t_dict.items():
#    out.write(b)
#    for w in t_list:
#      out.write('\t%d' % 999)
#    out.write('\n')
#  out.close()
out = open('blogdata.txt','w') 
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
# Write the words, separating with tabs. (Kinda like x axis.)
out.write('\n')
# Write a new line to separate the words you're counting with the rest of the doc
for blog, wc in wordcounts.items():
  # This loops thru the dict_items object of the wordcounts.
  # Wordcounts is a nested dictionary. Has a dictionary for each blog, that
  #   contains a dictionary of {<word> : <word count>} combinations.
  # So here, blog is the blog name, and wc is the dictionary of words and
  #   their counts.
  out.write(blog)
  # Write a line(?) for each blog name
  for word in wordlist:
    # For every word in the master word list,
    if word in wc: out.write('\t%d' % wc[word])
    # Write the word count if the word is in this blogs word count dictionary
    else: out.write('\t0')
    # Otherwise just write zero
  out.write('\n')
