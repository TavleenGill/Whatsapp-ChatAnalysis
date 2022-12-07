import helper
import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp chat Analyzer")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8") # converting byte stream into string
    df=preprocessor.preprocess(data)

    #st.dataframe(df)


    # Fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        #stats Area

        num_messages,words,num_media,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly Timeline
        st.title("Monthly Timeline")

        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['messages'],color='black')
        st.pyplot(fig)


        # Activity Map
        st.title("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy Month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='brown')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots(figsize=(12,6))
        #plt.figure(figsize=(5, 5))
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Finding busiest users in group (Group level)
        if selected_user=='Overall':
            st.title("Most busy Users")
            x,busy_user_df=helper.fetch_busy_user(df)
            fig,ax=plt.subplots()
            
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(busy_user_df)

        #WordCloud
        st.title("Word Cloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most Common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title("Most Common Words")
        st.pyplot(fig)
        #st.dataframe(most_common_df)

        #Emoji Analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')
        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)

 
