from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request
from nltk_summarization import nltk_summarizer
from spacy_summarization import text_summarizer
import time
import spacy
nlp = spacy.load('en_core_web_sm')
app = Flask(__name__)

# Web Scraping Pkg
from bs4 import BeautifulSoup
# from urllib.request import urlopen
from urllib.request import urlopen,Request



# Reading Time
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime

# Fetch Text From Url
def get_text(url):
	req=Request(url=url,headers= {"User-Agent": "Mozilla/5.0"})
	page = urlopen(req)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text
@app.route('/')
def home():
	return render_template('index.html')

@app.route('/text',methods=['GET','POST'])
def text():
	return render_template('index.html')

@app.route('/link',methods=['GET','POST'])
def link():
	return render_template('link.html')



@app.route('/analyze',methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext_t = request.form['rawtext']
		final_reading_time = readingTime(rawtext_t)
		final_summary_t = text_summarizer(rawtext_t)
		summary_reading_time = readingTime(final_summary_t)
		end = time.time()
		final_time = end-start

	return render_template('index.html',ctext_t=rawtext_t,final_summary_t=final_summary_t,final_time=final_time,final_reading_time_t=final_reading_time,summary_reading_time_t=summary_reading_time,show_result1 = True)

@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
	start = time.time()
	if request.method == 'POST':
		raw_url_u = request.form['raw_url']
		rawtext_u = get_text(raw_url_u)
		final_reading_time = readingTime(rawtext_u)
		final_summary_u = text_summarizer(rawtext_u)
		summary_reading_time = readingTime(final_summary_u)
		
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext_u=rawtext_u,final_summary_u=final_summary_u,final_time=final_time,final_reading_time_u=final_reading_time,summary_reading_time_u=summary_reading_time,show_result2 = True)








@app.route('/about')
def about():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True,port=5001)
