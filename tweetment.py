from flask import Flask,render_template,request
import os
import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import speech_recognition as sr
import pyaudio


app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])


def percentage(part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

def tweetment(hashtag,tweet_count):
    consumerKey = 'CHfvQADS2lWqWN3is8PEzHfut'
    consumerSecret = 'I7x5E2xWp79UoXPJ6kD9PRDrGJRAJ4BaPnD0HRf6nVyz3XDzEN'
    accessToken = '1002779913588359170-A6G6gLvVB14PPudT9Hx2uiflUBNLjb'
    accessTokenSecret = 'byZoa2mGNLSIJUkD0qDur4JGdBnjvx9PEHEEJMydLjVpn'
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
        print(searchTerm)
        print(NoOfTerms)
        

    print("ANALYSING...............................................................!!!!!!")

    tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
    print(searchTerm)
    print(NoOfTerms)
    #print(len([tweets]))

    polarity = 0
    positive = 0
    #wpositive = 0
    spositive = 0
    negative = 0
    #wnegative = 0
    snegative = 0
    neutral = 0

    count1=0
    for tweet in tweets:
        count1+=1
        print("count-------------------------------------------------------->",count1)
        #Append to temp so that we can store in csv later. I use encode UTF-8
        #tweetText.append(cleanTweet(tweet.text).encode('utf-8'))
        # print (tweet.text.translate(non_bmp_map))    #print tweet's text
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity
        #print(analysis.sentiment.polarity)
        
        
        if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
            neutral += 1
            print(analysis.sentiment.polarity,"neutral")
        #elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
            #wpositive += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.6):
            positive += 1
            print(analysis.sentiment.polarity,"positive")
        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
            spositive += 1
            print(analysis.sentiment.polarity,"spositive")
        #elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
            #wnegative += 1
        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity < 0):
            negative += 1
            print(analysis.sentiment.polarity,"negative")
        elif (analysis.sentiment.polarity >= -1 and analysis.sentiment.polarity <= -0.6):
            snegative += 1
            print(analysis.sentiment.polarity,"snegative")

            

    positive = percentage(positive, NoOfTerms)
    #wpositive = percentage(wpositive, NoOfTerms)
    spositive = percentage(spositive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    #wnegative = percentage(wnegative, NoOfTerms)
    snegative = percentage(snegative, NoOfTerms)
    neutral = percentage(neutral, NoOfTerms)

    # finding average reaction
    polarity = polarity / NoOfTerms


    if (polarity == 0):
        gp="Neutral"
    #elif (polarity > 0 and polarity <= 0.3):
        #gp="Weakly Positive"
    elif (polarity > 0 and polarity <= 0.6):
        gp="Positive"
    elif (polarity > 0.6 and polarity <= 1):
       gp="Strongly Positive"
    #elif (polarity > -0.3 and polarity <= 0):
       #gp="Weakly Negative"
    elif (polarity > -0.6 and polarity < 0):
       gp="Negative"
    elif (polarity >= -1 and polarity <= -0.6):
       gp="Strongly Negative"
        
        
    results=[searchTerm,NoOfTerms,gp]


    labels = ['Positive [' + str(positive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Strongly Negative [' + str(snegative) + '%]', 'Neutral [' + str(neutral) + '%]','Negative [' + str(negative) + '%]' ]
    sizes = [positive, spositive,snegative, neutral, negative ]
    colors = ['#64dd17','#1b5e20','#d50000', '#ffff00', 'red']

    
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = (0.0, 0.0, 0.0, 0.0,0.0)

    #add colors
    #colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

    #explode = (0.04,0.1,0.04,0.04,0.1)
    
    plt.pie(sizes, colors = colors, startangle=90, pctdistance=0.85, explode = explode)
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels,loc="lower right",bbox_to_anchor=(1.05, 0.5),fontsize='small')
    #draw circle
    centre_circle = plt.Circle((0,0),0.60)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')  
    files= os.listdir('static/img')
    if 'result.png' in files:
        os.remove('static/img/result.png')
    fig2 = plt.gcf()
    fig2.savefig('static/img/result.png',bbox_inches="tight",dpi=400,transparent=True)
    return results

#home() serves the home page(i.e index.html

@app.route('/')
def home():
    files= os.listdir('static/img/')
    if 'result.png' in files:
        os.remove('static/img/result.png')
    return render_template("index.html")


#send_static(filename) serves the files present in the static folder.
'''@app.route('/<filename :path>')
def send_static(filename):
    return static_file(filename, root = 'static/')'''

@app.route("/result",methods = ['POST'])
def analyize():
    if request.method == "POST":
        hashtag = request.form["hashtag"]
        tweet_count = request.form["tweet_count"]
    print(hashtag)
    print(tweet_count)
    res=tweetment(hashtag,tweet_count)
    return render_template("result.html",results=res)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
