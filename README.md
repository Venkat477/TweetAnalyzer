# Simple-WebCrawler
This is a simple Twitter Tweets Analyzer, which takes a Handler as an input and will provide below details in a detailed easy readable format.

***1. Most Recent Tweets <br />
2. Top 25 Tweets with most Likes <br />
3. Top 25 Tweets with most Re-Tweets <br />
4. Tweets with No Likes/Re-Tweets <br />
5. Tweets Sentiment Analysis Report <br />
6. Tweets Word Cloud Report***

This a basic project on how to extract tweets from Twitter using Twitter API and get some key and useful insights from the given handler. Using this, we can create much more neat twitter analytics solutions using different NLP Techniques.

This project is developed using Streamlit (https://www.streamlit.io/), an open-source framework which we can use to create a simple and neat UI without any HTML, CSS or JavaScript Knowledge. It is the easiest way for data scientists and machine learning engineers to create beautiful, performant apps in only a few hours!  All in pure Python. All for free.

I tried to include all the possible cases to extract the above information, but still for some cases it may fail.


***1. Used Regex Patterns for removing all the unwanted characters and to clean the tweets. <br />
2. Used Stop Words from NLTK module to remove stopwords from the Tweets. <br />
3. Used Pandas to process and query Tweets. <br />
4. Used Plotly and matplotlib to display Charts and Graphs. <br />
5. Used Python Tweepy Package to extract Tweets from Twitter***


**Programming Language:** Python3.7

Test the webapp using the given link (https://simplewebcrawler.herokuapp.com/)
