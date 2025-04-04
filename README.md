# WhatsApp Chat Analysis

## 📌 Project Overview
This project analyzes **individual and group chats** from WhatsApp. It processes exported `.txt` chat files, extracts structured data, and provides insights based on chat patterns. The application is deployed on Streamlit and can be accessed here:

[whatsapp-chat-analysis-insights-tool.streamlit.app](http://whatsapp-chat-analysis-insights-tool.streamlit.app/)

## 🕸️ Features
- Supports **individual and group chat** analysis.
- Extracts details such as **date, time, user messages, day, month, year, and period**.
- Handles multiple chat formats (12-hour AM/PM and 24-hour time formats).
- Provides a clean **Streamlit UI** for easy interaction.
- Error handling for different file upload issues.

## Project Structure
```
📂 whatsapp_chat_analysis/
│── app.py                      # Streamlit web application
│── preprocess.py               # Preprocessing logic for chat files
│── helper.py                   # Functions for analysis and insights
│── requirements.txt            # Required Python libraries
│── runtime.txt                 # Runtime environment settings
│── stop_words.txt              # Containing stop words for filtering
│── exporting_chat_readme.txt   # Instructions for exporting WhatsApp chats
│── images/                      # Folder containing images for chat export guide
```

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/whatsapp-chat-analysis.git
   ```
2. Navigate into the project folder:
   ```sh
   cd whatsapp-chat-analysis
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   streamlit run app.py
   ```

## How to Export WhatsApp Chat
Follow the instructions in `exporting_chat_readme` for exporting chats properly. You can also refer to images in `images/` for a step-by-step guide.

## Dependencies
A `requirements.txt` file is provided for easy installation. The environment is set in `runtime.txt`.

### `requirements.txt`
```
streamlit
pandas
matplotlib
seaborn
urlextract
numpy
wordcloud
emoji
```

### `runtime.txt`
```
python-3.11
```

## Contributions
Feel free to open an issue or pull request for improvements!

## JAYESH S CHAUHAN
