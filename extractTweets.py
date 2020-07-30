# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 18:20:31 2020
@author: Venkata N Divi
"""
from PIL import Image
import plotly.express as px
from textblob import TextBlob
from nltk import word_tokenize
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from tweepy import API,OAuthHandler
import preprocessor as p,re,string,sys,pandas as pd,streamlit as st

pd.set_option('display.max_colwidth', None)

#Twitter credentials for the app
consumer_key = 'kLb14rz8xHzGk9dpDj74UYwyZ'
consumer_secret = 'pu0o297R5zfUuWLbDHJ9IhjWP2E3M4p37YV71R8HgO6brgSCg5'
access_key= '186022911-yzD5on74EKkWA2Ac5IcJ3ocfdkJqJQjoKvdwOn0B'
access_secret = '7p1MYRWQvRivB30xTcfXYsPddZINzKTX0kl6iT5SY3spJ'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = API(auth)

stop = [word for word in set(stopwords.words('english')) if len(word)>1]

def clean_tweets(tweet):
    try:
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(tweet)
        tweet = re.sub(r':', '', tweet)
        tweet = re.sub(r'‚Ä¶', '', tweet)
        tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)     #replace consecutive non-ASCII characters with a space
        filtered_tweet = [w.replace('|','').replace('/','').replace('...','').strip() for w in word_tokens if w not in stop_words and w not in string.punctuation]
        
        return ' '.join(filtered_tweet)
    except Exception as e:
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)

def generateWordCloud(words):
    try:
        wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(words)
        plt.imshow(wordCloud, interpolation="bilinear")
        plt.axis('off')
        plt.savefig('WC.jpg')
        img= Image.open("WC.jpg") 
        return img
    except Exception as e:
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)

def getMostRecentTweets(hashtag,tweetCount):
    try:
        posts = api.user_timeline(screen_name=hashtag, count = tweetCount, lang ="en", tweet_mode="extended")
        tweetData = []
        for post in posts:
            result = {}
            result['created_at'],result['Tweet'],result['user'] = str(post.created_at),post.full_text,post.user.name
            result['retweetCount'],result['likeCount'] = post.retweet_count,post.favorite_count
            
            tweetData.append(result)

        topTweet_df = pd.DataFrame(tweetData)
        return topTweet_df
    except Exception as e:
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)

def getTweets(hashtag):    
    try:
        posts = api.user_timeline(screen_name=hashtag, count = 10000, lang ="en", tweet_mode="extended")
        tweetData = []
        for post in posts:
            result = {}
            result['created_at'],result['Tweet'],result['user'] = str(post.created_at),post.full_text,post.user.name
            result['screen_name'],result['location'],result['about'] = post.user.screen_name,post.user.location,post.user.description
            result['followers'],result['following'] = post.user.followers_count,post.user.friends_count
            result['retweetCount'],result['likeCount'] = post.retweet_count,post.favorite_count
            result['cleanedTweet'] = clean_tweets(p.clean(post.full_text))
            result['processedTweet'] = p.clean(post.full_text)
            
            blob = TextBlob(result['cleanedTweet'])
            Sentiment = blob.sentiment     
            polarity,subjectivity = Sentiment.polarity,Sentiment.subjectivity
            sentimentClass = 'Negative' if polarity < 0 else 'Positive' if polarity > 0 else 'Neutral'
            
            result['SentimentScore'],result['Polarity'],result['Subjectivity'] = sentimentClass,polarity,subjectivity
            tweetData.append(result)
    
        tweet_df = pd.DataFrame(tweetData)
        return tweet_df
    except Exception as e:
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)
        
def selectOptions():
    try:
        st.write("""You want the tweets like most recent, liked, re-tweeted, used words and want all 
                this information in a structural manner with an automate script. Then you are using the
                right thing.""")
        st.write("""This is a Tweet Analyzer, which takes a twitter handle as an input and provide detailed 
                analysis of the tweets to the user. Below are the details you can get.""")
        st.write("""
        - **Most Recent Tweets**
        - **Top 25 Tweets with most Likes**
        - **Top 25 Tweets with most Re-Tweets**
        - **Tweets with No Likes/Re-Tweets**
        - **Tweets Sentiment Analysis Report**
        - **Tweets Word Cloud Report**""")
        st.write("""When we got the handler, will use twitter API to extract all the recent tweets. 
            Based on it, by applying different NLP techniques like **Tokenization, TfIdf Vectorizer 
            and regex techniques** to clean the tweets and analyzing them.""")
        st.write("""One can develop any sort of extraction logic using above steps.""")
        st.subheader('**Use the Left Side Options to test the Service**')
    except Exception as e:
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)

def processTweets():
    try:
        st.subheader("**Try Our Service**")
        handler_ = st.text_input("Enter Twitter Handler")
        st.info('**Enter without @ (Ex:If Handler is @IBM, enter as IBM)**')
        choice_ = st.selectbox("Select the Activities",  ["Most Recent Tweets",
                        "Top 25 Tweets with most Likes","Top 25 Tweets with most Re-Tweets",
                        "Tweets with No Likes/Re-Tweets","Tweets Sentiment Analysis Report",
                        "Tweets Word Cloud Report"])

        if st.button('Analyze'):
            if len(handler_)>1:
                Tweet_df = getTweets(handler_)
                if choice_ == 'Most Recent Tweets':
                    st.success('Getting Most Recent Tweets')
                    top10_df = getMostRecentTweets(handler_,10)
                    st.table(top10_df)
                
                elif choice_ == "Top 25 Tweets with most Likes":
                    df1 = Tweet_df[['created_at','Tweet','cleanedTweet','user','likeCount']].sort_values('likeCount',ascending=False)
                    df1 = df1[:25]
                    dfMain = pd.DataFrame({'date':df1['created_at'],'likeCount':df1['likeCount']})
                    chart_data = dfMain.rename(columns={'date':'index'}).set_index('index')
                    st.bar_chart(chart_data)
                    
                    st.table(df1)
                
                elif choice_ == "Top 25 Tweets with most Re-Tweets":
                    df1 = Tweet_df[['created_at','Tweet','cleanedTweet','user','retweetCount']].sort_values('retweetCount',ascending=False)
                    df1 = df1[:25]
                    dfMain = pd.DataFrame({'date':df1['created_at'],'retweets':df1['retweetCount']})
                    chart_data = dfMain.rename(columns={'date':'index'}).set_index('index')
                    st.bar_chart(chart_data)
                    
                    st.table(df1)
                    
                elif choice_ == "Tweets with No Likes/Re-Tweets":
                    df1 = Tweet_df[['created_at','Tweet','cleanedTweet','user','likeCount','retweetCount']].loc[(Tweet_df['likeCount'] == 0) & (Tweet_df['retweetCount'] == 0)]
                    st.table(df1[:10])
                
                elif choice_ == "Tweets Sentiment Analysis Report":
                    Posdf1 = Tweet_df[['created_at','Tweet','cleanedTweet','user','Polarity','SentimentScore']].loc[(Tweet_df['SentimentScore'] == 'Positive')]
                    Negdf1 = Tweet_df[['created_at','Tweet','cleanedTweet','user','Polarity','SentimentScore']].loc[(Tweet_df['SentimentScore'] == 'Negative')]
                    Nuedf1 = Tweet_df[['created_at','Tweet','cleanedTweet','user','Polarity','SentimentScore']].loc[(Tweet_df['SentimentScore'] == 'Neutral')]
                    fig = px.pie(Tweet_df, values=[len(Posdf1),len(Negdf1),len(Nuedf1)], names=['Positive','Negative','Neutral'], color_discrete_sequence=px.colors.sequential.RdBu)
                    st.subheader('Out of **'+str(len(Posdf1)+len(Negdf1)+len(Nuedf1))+'** Tweets, **'+str(len(Posdf1))+'** were Positive, **'+str(len(Negdf1))+'** were Negative and **'+str(len(Nuedf1))+'** were Neutral Speaking Tweets')
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.write(len(Posdf1))
                    st.write(len(Negdf1))
                    st.write(len(Nuedf1))
                
                elif choice_ == "Tweets Word Cloud Report":
                    allwords = ' '.join(tweet for tweet in Tweet_df['cleanedTweet'])
                    img = generateWordCloud(allwords)
                    st.image(img, caption='Word Cloud for '+handler_,use_column_width=True)
            else:
                st.warning('Please try to enter valid Handler!!!')
                
    except Exception as e:
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)
    
def main():
    try:
        st.sidebar.title("Tweets Analyzer")
        st.sidebar.markdown("Try our Service!!!")
        st.sidebar.subheader("Choose")
        activities=["Select","Tweets Analyzer"]
        
        choice = st.sidebar.selectbox("",activities)
        if choice == 'Select':
            selectOptions()
        elif choice == 'Tweets Analyzer':
            processTweets()
    except Exception as e:
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)

if __name__ == '__main__':
    st.write('<!DOCTYPE html><html lang="en">   <head>      <meta charset="UTF-8">      <meta name="viewport" content="width=device-width, initial-scale=1.0">      <meta http-equiv="X-UA-Compatible" content="ie=edge">      <title>Responsive Navigation Bar - W3jar.Com</title>      <style>*,*::before,*::after {  box-sizing: border-box;  -webkit-box-sizing: border-box;}body {  font-family: sans-serif;  margin: 0;  padding: 0;}.container {  height: 80px;  background-color: #052252;  display: -webkit-box;  display: -ms-flexbox;  display: flex;  -ms-flex-wrap: wrap;  flex-wrap: wrap;  -webkit-box-align: center;  -ms-flex-align: center;  align-items: center;  overflow: hidden;}.container .logo {  max-width: 250px;  padding: 0 10px;  overflow: hidden;}.container .logo a {  display: -webkit-box;  display: -ms-flexbox;  display: flex;  -ms-flex-wrap: wrap;  flex-wrap: wrap;  -webkit-box-align: center;  -ms-flex-align: center;  align-items: center;  height: 60px;}.container .logo a img {  max-width: 100%;  max-height: 60px;}@media only screen and (max-width: 650px) {  .container {    -webkit-box-pack: justify;    -ms-flex-pack: justify;    justify-content: space-between;  }  .container .logo {    -webkit-box-flex: 1;    -ms-flex: 1;    flex: 1;  }}.body {  max-width: 700px;  margin: 0 auto;  padding: 10px;} .h1 { color:#FEFEFE; position: center; top: 10px; font-size:135px;font-family:verdana;    margin-top:0px;    margin:0px; line-height:50px; }</style>   </head>   <body>      <div class="container">      <div class="logo">    <a href="#"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLjlSh59xixv6raIujNPqBlW1toVmAnhK07ckT-OunDgSAm1w&s" alt="logo"></a>    </div> </body></html>', unsafe_allow_html=True)
    st.title("Tweets Analyzer")
    st.markdown("You have a Twitter Handle and want to analyze the tweets? **Try our Service!!!**")
    main()
