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


# Returns title and dictionary of word counts for an RSS feed
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
  return(d.feed.title,wc)


def getwords(html):
  # Remove all the HTML tags
  txt=re.compile(r'<[^>]+>').sub('',html)
  # Split words by all non-alpha characters
  words=re.compile(r'[^A-Z^a-z]+').split(txt)
  # Convert to lowercase
  return([word.lower() for word in words if word!=''])

apcount={}
wordcounts={}
for feedurl in file('feedlist.txt'):
  # Not sure what file() should be in python 3, BUT the idea here is to iterate
  #   thru each line in the .txt file. Can probs figure out a way to do that.
  #   each line here is just a string containing a url.
  title,wc=getwordcounts(feedurl)
  wordcounts[title]=wc
  for word,count in wc.items():
    apcount.setdefault(word,0)
    if count>1:
      apcount[word]+=1


wordlist=[]
for w,bc in apcount.items():
  frac=float(bc)/len(feedlist)
  if frac>0.1 and frac<0.5: wordlist.append(w)

out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
  out.write(blog)
  for word in wordlist:
    if word in wc: out.write('\t%d' % wc[word])
    else: out.write('\t0')
out.write('\n')

# -----------------------------------------------------------------------------
