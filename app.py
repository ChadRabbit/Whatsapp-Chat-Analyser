import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns
import wordcloud
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocessor(data)
    st.dataframe(df)
    #Fetching unique users
    userList=df['user'].unique().tolist()
    userList.sort()
    userList.insert(0,"Overall")
    option = st.sidebar.selectbox("Show analysis for?",userList)
    if st.sidebar.button("Show Analysis"):
        total_msg,total_words,total_media,total_link=helper.fetch_stats(option,df)
        col1,col2,col3,col4=st.columns(spec=4)
        with col1:
            st.header("Total Messages")
            st.title(total_msg)
        with col2:
            st.header("Total Words")
            st.title(total_words)
        with col3:
            st.header("Total Media Files")
            st.title(total_media)
        with col4:
            st.header("Total Links")
            st.title(total_link)
        if option=='Overall':
            st.title('Busiest User')
            col1,col2=st.columns(2)
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        df_wc=helper.create_wordcloud(option,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.title('WordCloud')
        st.pyplot(fig)
        #Most Common Words
        most_common_words=helper.most_common_words(option,df)
        st.title("Most Commonly Used Words")
        fig,ax=plt.subplots()
        ax.barh(most_common_words[0],most_common_words[1])
        st.pyplot(fig)
        #Emoji Analayses
        emoji_df=helper.most_emoji(option,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1],labels=emoji_df[0])
            st.pyplot(fig)
        #MONTHLY TIMELINE
        st.title("TIMELINE ANALYSIS")
        timeline=helper.monthly_timeline(option,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #DAILY TIMELINE
        st.title("DAILY ANALYSIS")
        daily_timeline=helper.daily_timeline(option,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['messages'],color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #ACTIVVITY MAP
        st.title("Activity ANALYSIS")
        busy_day,busy_month=helper.activity_analysis(option,df)
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most monthly day")
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #HEATMAP
        st.title("HEATMAP OF USER")
        heatmap=helper.activity_heatmap(option,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(heatmap)
        st.pyplot(fig)


