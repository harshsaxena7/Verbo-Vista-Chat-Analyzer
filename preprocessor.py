import re
import pandas as pd
import streamlit as st

def preprocess(data):
    try:
        if not data.strip():  # strip() removes any whitespace/newlines
            st.error("⚠️ Uploaded file is empty. Please upload a valid chat file.")
            return None
        
        # Define both possible patterns
        pattern1 = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s?[APap][Mm]) - (.*)"
        pattern2 = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}) - (.*)"
        
        # Try matching with the first pattern
        matches = re.findall(pattern1, data)
        if not matches:
            # If first pattern fails, try second pattern
            matches = re.findall(pattern2, data)
        
        if not matches:
            st.error("⚠️ No valid chat format found. Please check the file.")
            return None
            
        df = pd.DataFrame(matches, columns=["Date", "Time", "Message"])
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        if df['Date'].isna().all():
            st.error("⚠️ Invalid date format in file. Unable to process.")
            return None
            # return "Invalid date format in file. Unable to process."

        df['Full_date'] = df['Date'].dt.date 
        df['Year'] = df['Date'].dt.year
        df['Month_name'] = df['Date'].dt.month_name()
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['Day_name'] = df['Date'].dt.day_name()
        df['Hour'] = df['Time'].str.extract(r'(\d{1,2}):')
        df['Minute'] = df['Time'].str.extract(r':(\d{2})')
        df['AM/PM'] = df['Time'].str.extract(r'(AM|PM)')
        
        df['Hour'] = pd.to_numeric(df['Hour'], errors='coerce')
        df['Minute'] = pd.to_numeric(df['Minute'], errors='coerce')
        
        period = []
        for hour, am_pm in zip(df['Hour'], df['AM/PM']):
            if pd.notna(hour):
                next_hour = 1 if hour == 12 else hour + 1
                period.append(f"{hour}-{next_hour} {am_pm if pd.notna(am_pm) else ''}")
            else:
                period.append('Unknown')
                
        df['Period'] = period
        df.drop('Date', axis=1, inplace=True)

        users = []
        messages = []
        for msg in df['Message']:
            entry = re.split('([\w\W]+?):\s', msg)
            if entry[1:]:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append('Group_notification')
                messages.append(entry[0])

        df['User'] = users
        df['Message'] = messages
        
        new_order = ["User", "Message", "Day", "Day_name", "Month", "Month_name", "Year", "Full_date", "Time", "Hour", "Minute", "AM/PM", "Period"]
        df = df[new_order]
        
        return df
    except Exception as e:
        st.error(f"⚠️ File appears to be corrupted or unreadable. Error: {str(e)}")
        return None  # Return None for errors
