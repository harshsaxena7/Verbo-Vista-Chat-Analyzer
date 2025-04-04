import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import preprocessor, helper
import altair as alt
from textblob import TextBlob

# Set page layout
st.set_page_config(layout="wide")
st.sidebar.title("📊 Verbo Vista Chat Analyzer")  # Changed name here

# File uploader
uploaded_file = st.sidebar.file_uploader("📁 Choose a File", type=["txt"])

# Max file size check
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
if uploaded_file:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("⚠ File size too large! Please upload a file smaller than 200MB.")
    else:
        # Process the uploaded file
        df = preprocessor.preprocess(uploaded_file.getvalue().decode("utf-8"))

        # Check if DataFrame is valid
        if df is not None and not df.empty:
            st.success("✅ Chat data loaded successfully!")
        else:
            st.error("❌ Error: Could not process the file! Please check the format.")
            st.stop()

        # Ensure "User" column exists
        if "User" not in df.columns:
            st.error("❌ No user data found! Please upload a valid chat file.")
            st.stop()

        # Create user selection dropdown
        user_list = df["User"].unique().tolist()
        user_list = [u for u in user_list if u.strip()]  # Remove empty names
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("👤 Select User:", user_list)

        if not selected_user:
            st.error("⚠ No user selected! Choose a user from the dropdown.")
            st.stop()

        if st.sidebar.button("📊 Show Analysis"):
            st.title("📊 Verbo Vista Chat Analysis")  # Changed title here

            # Fetch statistics
            num_messages, words, num_media, links = helper.show_stat(selected_user, df)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📩 Messages", num_messages)
            with col2:
                st.metric("📝 Words", words)
            with col3:
                st.metric("📸 Media Shared", num_media)
            with col4:
                st.metric("🔗 Links Shared", links)

            # Most active users
            if selected_user == "Overall":
                st.header("📌 Most Active Users")
                col1, col2 = st.columns(2)

                x1, x2 = helper.show_busy_user(df)
                
                # Plot the first chart (Most active users)
                with col1:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.bar(x1.index, x1.values, color="skyblue")
                    ax.set_xlabel("Users")
                    ax.set_ylabel("Message Count")
                    ax.tick_params(axis='x', rotation=90)
                    st.pyplot(fig)

            # Word cloud
            st.header("☁ Word Cloud")
            df_wc = helper.show_word_cloud(selected_user, df)
            if df_wc:
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.imshow(df_wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.warning("😭 No words available to generate Word Cloud.")

            # Most Common Words
            st.header("📌 Most Common Words")
            common_words_df = helper.show_most_com_word(selected_user, df)
            if not common_words_df.empty:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.barplot(x=common_words_df["Count"], y=common_words_df["Word"], ax=ax, palette="Blues_r")
                ax.set_xlabel("Count")
                ax.set_ylabel("Words")
                st.pyplot(fig)
            else:
                st.warning("😭 No common words found.")

            # Emoji Analysis
            st.header("😀 Emoji Analysis")
            emoji_df = helper.show_emoji_ana(selected_user, df)
            if not emoji_df.empty:
                st.dataframe(emoji_df)
            else:
                st.warning("😭 No emoji data available.")

            # Timeline Analysis
            st.header("📆 Timeline Analysis")
            timeline = helper.show_month_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(timeline["Time"], timeline["Message"], marker="o", linestyle="-", color="green")
            ax.set_xlabel("Time")
            ax.set_ylabel("Messages")
            ax.tick_params(axis='x', rotation=90)
            st.pyplot(fig)

            # Sentiment Analysis
            st.header("🔍 Sentiment Analysis")
            df["Sentiment"] = df["Message"].apply(lambda x: TextBlob(x).sentiment.polarity)
            sentiment_counts = df["Sentiment"].apply(lambda x: "Positive" if x > 0 else ("Negative" if x < 0 else "Neutral")).value_counts()

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", colors=["green", "red", "gray"])
            ax.set_title("Sentiment Distribution")
            st.pyplot(fig)

            # Emotion Detection (NEW FEATURE)
            st.header("🎭 Emotion Detection")
            from transformers import pipeline
            emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
            df["Emotion"] = df["Message"].apply(lambda x: emotion_model(x)[0]["label"] if len(x) > 10 else "Neutral")

            emotion_counts = df["Emotion"].value_counts()
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(x=emotion_counts.index, y=emotion_counts.values, ax=ax, palette="viridis")
            ax.set_xlabel("Emotions")
            ax.set_ylabel("Count")
            st.pyplot(fig)

            st.success("✅ Analysis Complete!")
