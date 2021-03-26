# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 09:38:36 2021

@author: sree
"""
import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import time

consumer_key = "Nj3kha2CYN94LBW2M54ezRPhO"
consumer_secret = "4PqwK44LqtxNmhxFbOQC3EwJockvcLZA5bLvmVAy9EjH89Ia1y"
access_token = "1108075687380836352-5pDD452FKejmf9GXo3hiTNFqwEGtYF"
access_token_secret = "JaOVt7P3GTx0oX65OrOPzqRwVRNKsYErt3NXeuMnc1w2z"

#Authentication

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#Create API object
api = tweepy.API(auth,wait_on_rate_limit = True)

def app():    
    st.title("Twitter Tweet Analyzer")
    
    sidebaroption = ["Analyze Tweet", "Twitter Data Generator"]
    selection = st.sidebar.selectbox("Select your option", sidebaroption)    
    if selection == "Analyze Tweet":
        
        st.subheader("Use this tool to analyze your favorite twitter personality")
        st.write("I) The most recent tweets are fetched from the handler given")
        st.write("II) Word Cloud Display Options is enabled")
        st.write("III) Visualization of the tweets in a bar chart based on the sentiment analysis")


		
        handler_id = st.text_area("Input the twitter handle of the Personality. Please DO NOT add the (@).")
        analysis_choice = st.selectbox("Select the Activities",  ["Display Recent Tweets","WordCloud Generation" ,"Sentiment Analysis Visualization"])
        if st.button("Analyze"):
            if analysis_choice == "Display Recent Tweets":
              #   latest_iteration = st.empty()
              #   bar = st.progress(0)
                
              #   for i in range(100):
                    
              # # Update the progress bar with each iteration.
              #       latest_iteration.text(f'Loading {i+1}')
              #       bar.progress(i + 1)
              #       time.sleep(0.1)
                    
                st.success("Fetched last 5 Tweets")
                
                def Show_Tweets(handler_id):                    
                    posts = api.user_timeline(screen_name= handler_id,count = 100, lang='en',tweet_mode="extended")                
                    def get_tweets():
                        # df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
                        l = []                    
                        for tw in posts[:5]:
                            l.append(tw.full_text)
                        return l
                        # return df.head()
                    recent_tweets = get_tweets()
                    return recent_tweets                  
                
                recent_tweets = Show_Tweets(handler_id)                
                # st.write(recent_tweets)
                recent_tweets
            
            elif analysis_choice == "WordCloud Generation":
                st.success("The World Cloud Generation")
                def World_Cloud(handler_id):
                    posts = api.user_timeline(screen_name= handler_id,count = 100, lang='en',tweet_mode="extended")                
                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
                    def cleantext(text):
                        
                        text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
                        text = re.sub('#', '', text) # Removing '#' hash tag
                        text = re.sub('RT[\s]+', '', text) # Removing RT
                        text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
                        
                        return text
                    
                    df['Tweets'] = df['Tweets'].apply(cleantext)
                    
                    allwords = ' '.join([twt for twt in df["Tweets"]])
                    worldCloud = WordCloud(width=800,height = 500,random_state=21,max_font_size=120).generate(allwords)
                    plt.imshow(worldCloud, interpolation="bilinear")
                    plt.axis('off')
                    plt.savefig("WC.JPEG")
                    imgopen = Image.open("WC.JPEG")
                    return imgopen
                imgDisp = World_Cloud(handler_id)
                st.image(imgDisp)
                
            else:
                st.success("The Sentiment Analysis Visualization is ready")
                
                def Sentiment_Visualization():
                    posts = api.user_timeline(screen_name= handler_id,count = 100, lang='en',tweet_mode="extended")                
                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
                    def cleantext(text):
                        
                        text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
                        text = re.sub('#', '', text) # Removing '#' hash tag
                        text = re.sub('RT[\s]+', '', text) # Removing RT
                        text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
                        
                        return text
                    
                    df['Tweets'] = df['Tweets'].apply(cleantext)
                    
                    def getSubjectivity(text):
                        return TextBlob(text).sentiment.subjectivity
                    df["Subjectivity"] = df["Tweets"].apply(getSubjectivity)
                    
                    def getPolarity(text):
                        return  TextBlob(text).sentiment.polarity
                    
                    df["Polarity"] = df["Tweets"].apply(getPolarity)
                    
                    def captureAnalysis(score):
                        if score < 0:
                            return "Negative"
                        elif score == 0:
                            return "Neutral"
                        else:
                            return "Positive"
                    df["Analysis"] = df["Polarity"].apply(captureAnalysis)
                                        
                    return df
                dfanalysis = Sentiment_Visualization()
                sns.set_theme(style="whitegrid")
                st.write(sns.countplot(x=dfanalysis['Analysis'], data=dfanalysis, linewidth=2, edgecolor=sns.color_palette("dark", 3),palette="Set3"))
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot(use_container_width=True)
    
    else:
        
        st.subheader("Export 100 tweets from the twitter handle to performs actions below")
        st.write("Use Pandas Dataframe")
        st.write("Use Regular Expression to clean the data")
        st.write("Analyze the Subjectivity of tweets extracted")
        st.write("Analyze the Polarity of tweets extracted")
        st.write("Analyze the Sentiment Analysis of tweets extracted")
        st.write("Display in a table format")

        
        handler_id = st.text_area("Input the twitter handle of the Personality. Please DO NOT add the (@).")
        
        
        def get_displaydata(handler_id):
            posts = api.user_timeline(screen_name= handler_id,count = 100, lang='en',tweet_mode="extended")                
            df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
            def cleantext(text):
                
                text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
                text = re.sub('#', '', text) # Removing '#' hash tag
                text = re.sub('RT[\s]+', '', text) # Removing RT
                text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
                
                return text
            
            df['Tweets'] = df['Tweets'].apply(cleantext)
            
            def getSubjectivity(text):
                return TextBlob(text).sentiment.subjectivity
            df["Subjectivity"] = df["Tweets"].apply(getSubjectivity)
            
            def getPolarity(text):
                return  TextBlob(text).sentiment.polarity
            
            df["Polarity"] = df["Tweets"].apply(getPolarity)
            
            def captureAnalysis(score):
                if score < 0:
                    return "Negative"
                elif score == 0:
                    return "Neutral"
                else:
                    return "Positive"
            df["Analysis"] = df["Polarity"].apply(captureAnalysis)
                                
            return df
        
        if st.button("Display Tweet"):
 
            latest_iteration = st.empty()
            bar = st.progress(0)
             
            for i in range(100):
                
             
            # Update the progress bar with each iteration.
                latest_iteration.text(f'Loading {i+1}')
                bar.progress(i + 1)
                time.sleep(0.1)
            
            dfdisplay = get_displaydata(handler_id)
            st.write(dfdisplay)      
        
        
    st.subheader(' ---------------------------------- MAP Team Twitter Analyzer -------------------------------- ')
        
    

if __name__ == "__main__":
    app()






