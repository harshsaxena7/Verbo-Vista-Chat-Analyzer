from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

# Function will show the statistic part of data
def show_stat(selected_user, df):
    try:
        if 'User' not in df.columns or 'Message' not in df.columns:
            return "Error: Required columns are missing from the data."

        if selected_user != 'Overall':
            df = df[df['User'] == selected_user]

        total_msg = df.shape[0]

        total_word_list = []
        for msg in df['Message']:
            total_word_list.extend(msg.split())

        total_word = len(total_word_list)
        total_media_file = df[df['Message'] == '<Media omitted>'].shape[0]

        extractor = URLExtract()
        link_list = []
        for msg in df['Message']:
            link_list.extend(extractor.find_urls(msg))

        link = len(link_list)
        return total_msg, total_word, total_media_file, link

    except Exception as e:
        return f"An error occurred in show_stat: {str(e)}"

# Function will show the most busy user
def show_busy_user(df):
    try:
        if 'User' not in df.columns:
            return None, None  # Return empty values if the 'User' column is missing

        # Get top 5 active users
        user_counts = df['User'].value_counts()
        
        if user_counts.empty:
            return None, None  # No user data available
        
        x1 = user_counts.head(5)  # Top 5 users
        df_percentage = round((user_counts / user_counts.sum()) * 100, 2).reset_index()
        df_percentage.columns = ['User', 'Percentage']
        
        return x1, df_percentage
    
    except Exception as e:
        print(f"Error in show_busy_user: {e}")
        return None, None
    
# Function will show word cloud 
def show_word_cloud(selected_user, df):
        try:
            if 'User' not in df.columns or 'Message' not in df.columns:
                return "Error: Required columns are missing from the data."
            
            if selected_user != 'Overall':
                df = df[df['User'] == selected_user]  # Fix filtering syntax

            # Remove non-text messages
            temp_df = df[(df['User'] != 'Group_notification') & (df['Message'] != '<Media omitted>')]

            # Read stop words
            with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
                stop_word = set(f.read().split())  # Convert to a set for faster lookup

            def remove_stop_word(msg):
                return " ".join([word for word in msg.lower().split() if word not in stop_word])

            # Apply text filtering
            temp_df['Message'] = temp_df['Message'].apply(remove_stop_word)

            # Check if there is any valid text left
            if temp_df['Message'].str.strip().str.len().sum() == 0:
                return None  # No valid text to generate a word cloud

            # Generate word cloud
            wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
            df_wc = wc.generate(temp_df['Message'].str.cat(sep=" "))
            return df_wc
        
        except Exception as e:
            return f"An error occurred in show_word_cloud: {str(e)}"

# Function will show most common words
def show_most_com_word(selected_user, df):
    try:
        if 'User' not in df.columns or 'Message' not in df.columns:
            return "Error: Required columns are missing from the data."
        
        if selected_user != 'Overall':
            df = df[df['User'] == selected_user]  

        # Remove non-text messages
        temp_df = df[(df['User'] != 'Group_notification') & (df['Message'] != '<Media omitted>')]

        # Read stop words
        with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
            stop_word = set(f.read().split())  

        def remove_stop_word(msg):
            return " ".join([word for word in msg.lower().split() if word not in stop_word])

        temp_df['Message'] = temp_df['Message'].apply(remove_stop_word)

        # Flatten all words into a single list
        words = " ".join(temp_df['Message']).split()

        if not words:  # If no words exist, return an empty DataFrame
            return pd.DataFrame(columns=['Word', 'Count'])

        # Count most common words
        most_common = Counter(words).most_common(10)
        
        return pd.DataFrame(most_common, columns=['Word', 'Count'])

    except Exception as e:
            return f"An error occurred in show_most_com_word: {str(e)}"

# Function will show emoji analysis
def show_emoji_ana(selected_user, df):
    try:
        if 'User' not in df.columns or 'Message' not in df.columns:
            return "Error: Required columns are missing from the data."

        if selected_user != 'Overall':
            df = df[df['User'] == selected_user]

        emoji_list = [c for msg in df['Message'] for c in msg if c in emoji.EMOJI_DATA]
        emj = pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))))
        return emj

    except Exception as e:
        return f"An error occurred in show_emoji_ana: {str(e)}"

# Function will show monthly timeline
def show_month_timeline(selected_user, df):
    try:
        if 'User' not in df.columns or 'Message' not in df.columns:
            return "Error: Required columns are missing from the data."

        if selected_user != 'Overall':
            df = df[df['User'] == selected_user]

        timeline = df.groupby(['Year', 'Month_name', 'Month']).count()['Message'].reset_index()
        timeline['Time'] = timeline.apply(lambda x: f"{x['Month_name']}-{x['Year']}", axis=1)
        return timeline

    except Exception as e:
        return f"An error occurred in show_month_timeline: {str(e)}"

# Function will show daily timeline
def show_day_timeline(selected_user, df):
    try:
        if 'User' not in df.columns or 'Message' not in df.columns:
            return "Error: Required columns are missing from the data."

        if selected_user != 'Overall':
            df = df[df['User'] == selected_user]

        return df.groupby(df['Full_date']).count()['Message'].reset_index()

    except Exception as e:
        return f"An error occurred in show_day_timeline: {str(e)}"

# Function will show activity per day of week
def show_day_name_ana(selected_user, df):
    try:
        if 'User' not in df.columns or 'Day_name' not in df.columns:
            return "Error: Required columns are missing from the data."

        if selected_user != 'Overall':
            df = df[df['User'] == selected_user]

        return df['Day_name'].value_counts()

    except Exception as e:
        return f"An error occurred in show_day_name_ana: {str(e)}"

# Function will show activity per month
def show_month_name_ana(selected_user, df):
    try:
        if 'User' not in df.columns or 'Month_name' not in df.columns:
            return "Error: Required columns are missing from the data."

        if selected_user != 'Overall':
            df = df[df['User'] == selected_user]

        return df['Month_name'].value_counts()

    except Exception as e:
        return f"An error occurred in show_month_name_ana: {str(e)}"

# Function will show activity at different time periods
def time_wise_active(selected_user, df):
    try:
        if 'User' not in df.columns or 'Message' not in df.columns or 'Period' not in df.columns:
            return "Error: Required columns are missing from the data."

        if selected_user != 'Overall':
            df = df[df['User'] == selected_user]

        return df.pivot_table(index='Day_name', columns='Period', values='Message', aggfunc='count').fillna(0)

    except Exception as e:
        return f"An error occurred in time_wise_active: {str(e)}"
