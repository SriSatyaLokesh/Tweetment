from flask import Flask,render_template,request
import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import speech_recognition as sr
import pyaudio

app = Flask(__name__,static_url_path="", static_folder="static")

def percentage(part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

def tweetment(hashtag,tweet_count):
    consumerKey = 'NkvxffCqoT8CF2r8tPY3f8irj'
    consumerSecret = 'PU86dNRPgLs5J3jWeGRkLKsI0RJdGcnmCmIvs8OIlpsHnwbQ5O'
    accessToken = '839523289701593088-5ccSCjUcECkOhbvy9GDagdNcLDth51L'
    accessTokenSecret = '1bym1DmOAsn89edExXFY9dGbyjl0nliqsCvc216WtZVKm'
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)


    #temp=input("Press 0/v/V for voice input for Text input:")
            
    if  1 < 0 :
        r = sr.Recognizer()
        searchTerm=""
        with sr.Microphone() as source:
            print("Speak Keyword/Tag to search about:")
            words = r.listen(source)        
            try:
                searchTerm = r.recognize_google(words)
                print("We are searching for:",searchTerm)             
            except:
                print("Sorry could not recognize what you said please enter manually......")
                searchTerm = input("Enter Keyword/Tag to search about: ")            
                
            print("how many tweets to search: ")
            nos=r.listen(source)        
            try:
                NoOfTerms=int(r.recognize_google(nos))
                print("Total no of tweets:",NoOfTerms)
            except:
                print("Sorry could not recognize what you said please enter manually......")
                NoOfTerms = int(input("Enter how many tweets to search: "))        
            
    else:       
        searchTerm = str(hashtag)
        NoOfTerms = int(tweet_count)

    print("ANALYSING...............................................................!!!!!!")

    tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

    polarity = 0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0


    for tweet in tweets:
        #Append to temp so that we can store in csv later. I use encode UTF-8
        #tweetText.append(cleanTweet(tweet.text).encode('utf-8'))
        # print (tweet.text.translate(non_bmp_map))    #print tweet's text
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity
        
        
        if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
            neutral += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
            wpositive += 1
        elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
            positive += 1
        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
            spositive += 1
        elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
            wnegative += 1
        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
            negative += 1
        elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
            snegative += 1
            

    positive = percentage(positive, NoOfTerms)
    wpositive = percentage(wpositive, NoOfTerms)
    spositive = percentage(spositive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    wnegative = percentage(wnegative, NoOfTerms)
    snegative = percentage(snegative, NoOfTerms)
    neutral = percentage(neutral, NoOfTerms)

    # finding average reaction
    polarity = polarity / NoOfTerms


    print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
    print()
    print("General Report: ")

    if (polarity == 0):
        print("Neutral")
    elif (polarity > 0 and polarity <= 0.3):
        print("Weakly Positive")
    elif (polarity > 0.3 and polarity <= 0.6):
        print("Positive")
    elif (polarity > 0.6 and polarity <= 1):
        print("Strongly Positive")
    elif (polarity > -0.3 and polarity <= 0):
        print("Weakly Negative")
    elif (polarity > -0.6 and polarity <= -0.3):
        print("Negative")
    elif (polarity > -1 and polarity <= -0.6):
        print("Strongly Negative")
        
        
    
    labels = ['Positive [' + str(positive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]','Negative [' + str(negative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
    sizes = [positive, spositive, neutral, negative, snegative]
    colors = ['#64dd17','#1b5e20', '#ffff00', 'red','#d50000']

    
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = (0.0, 0.0, 0.0, 0.0,0.0)

    #add colors
    #colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

    #explode = (0.04,0.1,0.04,0.04,0.1)
    
    plt.pie(sizes, colors = colors, startangle=90, pctdistance=0.85, explode = explode)
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels,loc="lower right",bbox_to_anchor=(1.05, 0.5),fontsize='small')
    #draw circle
    centre_circle = plt.Circle((0,0),0.60,fc='#33ccff')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')  
    plt.tight_layout()
    fig.savefig('static/img/result.png',dpi=400,transparent=True)

#home() serves the home page(i.e index.html page on start).
@app.route("/")
def home():
    return render_template("index")


@app.route("/result",method="POST")
def analyize():
    hashtag = request.forms.get("hashtag")
    tweet_count = request.forms.get("tweet_count")
    print(hashtag)
    print(tweet_count)
    tweetment(hashtag,tweet_count)
    return render_template("result")

if __name__ == '__main__':
	app.run(ost = "localhost", reloader = "True", port = 8000)
