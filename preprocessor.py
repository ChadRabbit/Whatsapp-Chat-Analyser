import pandas as pd
import re
def preprocessor(data):
    pattern='[0-9]+/[0-9]+/[0-9]+,\s[0-9]+:[0-9]+[\s\u202F][a|p]m\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date'] = df['message_date'].str.strip(' - ')
    df['message_date']=pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p')
    users=[]
    messages=[]
    for message in df['user_message']:
        pattern_msg = r'^([.\s]?[\w\s~]+?):\s'
        entry=re.split(pattern_msg,message)
        if len(entry)>1:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group_Notification')
            messages.append(entry[0])
    period=[]

    df['user']=users
    df['messages']=messages
    df.drop(columns=['user_message'],inplace=True)
    df['year']=df['message_date'].dt.year
    df['month']=df['message_date'].dt.month_name()
    df['date']=df['message_date'].dt.day
    df['hour']=df['message_date'].dt.hour
    df['minute']=df['message_date'].dt.minute
    df['month_num']=df['message_date'].dt.month
    df['only_date']=df['message_date'].dt.date
    df['day_names']=df['message_date'].dt.day_name()
    for hour in df[['day_names','hour']]['hour']:
        if(hour==23):
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str(00)+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period']=period
    return df
