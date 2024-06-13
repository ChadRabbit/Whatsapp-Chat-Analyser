from urlextract import URLExtract
import pandas as pd
import matplotlib.pyplot as plt
import emoji
from collections import Counter
import seaborn as sns
from wordcloud import WordCloud
def fetch_stats(selected_user,df):
    if(selected_user!='Overall'):
        df=df[df['user']==selected_user]
    total_words=0
    total_media=0
    total_link=0
    extractor=URLExtract()
    for message in df['messages']:
        if message=='<Media omitted>\n':
            total_media+=1
        total_words+=len(message.split())
        total_link+=len(extractor.find_urls(message))
    return df.shape[0],total_words,total_media,total_link

def most_busy_users(df):
    x=df['user'].value_counts()[:5]
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if(selected_user!='Overall'):
        df=df[df['user']==selected_user]
    temp_df=df[df['user']!='Group_Notification']
    temp_df=temp_df[temp_df['messages']!='<Media omitted>\n']
    def remove_stop_words(messages):
        y=[]
        f=open('stop_hinglish.txt','r')  #Ignore commonly used stop words of english/hindi
        stop_words=f.read()
        for word in messages.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    temp_df['messages']=temp_df['messages'].apply(remove_stop_words)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(temp_df['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if(selected_user!='Overall'):
        df=df[df['user']==selected_user]
    temp_df=df[df['user']!='Group_Notification'] #Omit Group Notifications
    temp_df=temp_df[temp_df['messages']!='<Media omitted>\n'] #Omit the "Media Omitted" message
    f=open('stop_hinglish.txt','r')  #Ignore commonly used stop words of english/hindi
    stop_words=f.read()
    words=[]
    for message in temp_df['messages']:   #To get each message in the df of messages
        for word in message.lower().split(): #To get each word in message
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))
def most_emoji(selected_user,df):
    if(selected_user!='Overall'):
        df=df[df['user']==selected_user]
    emj=[]
    for message in df['messages']:
        tp=emoji.emoji_list(message)
        for item in tp:
            emj.append(item['emoji'])

    return pd.DataFrame(Counter(emj).most_common(20))

def monthly_timeline(selected_user,df):
    if(selected_user!='Overall'):
        df=df[df['user']==selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if(selected_user!='Overall'):
        df=df[df['user']==selected_user]
    daily_timeline=df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline
def activity_analysis(selected_user,df):
    if(selected_user!='Overall'):
        df=df[df['user']==selected_user]
    return df['day_names'].value_counts(),df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if(selected_user!='Overall'):
        df=df[df['user']==selected_user]
    heatmap=(df.pivot_table(index='day_names',columns='period',values='messages',aggfunc='count').fillna(0))
    return heatmap
