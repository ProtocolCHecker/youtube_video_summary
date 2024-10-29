import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# Function to fetch and parse the summarized content
def get_summarized_content(youtube_url):
    # Construct summarize.tech URL for the YouTube video
    summarize_url = f'https://www.summarize.tech/{youtube_url}'
    
    # Headers for the request
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-GB,en;q=0.5',
        'priority': 'u=0, i',
        'referer': 'https://www.summarize.tech/',
        'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    # Attempt to get a response, checking every 10 seconds for up to 10 minutes
    response = None
    for attempt in range(60):  # 60 attempts (10 minutes at 10-second intervals)
        try:
            response = requests.get(summarize_url, headers=headers)
            if response.status_code == 200:
                break  # Exit the loop if a successful response is received
        except requests.exceptions.RequestException as e:
            st.write(f"Attempt {attempt+1}: Waiting for the website to respond...")
        time.sleep(10)  # Wait for 10 seconds before retrying

    # Check if a response was received after the loop
    if response is None or response.status_code != 200:
        st.error("Failed to retrieve a response from the website. Please try again later.")
        return "", pd.DataFrame()  # Return empty values if no response

    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the overall summary from the first <p> tag within the relevant <section>
    overall_summary = ""
    summary_section = soup.find('section')
    if summary_section:
        overall_summary_paragraph = summary_section.find('p')
        if overall_summary_paragraph:
            overall_summary = overall_summary_paragraph.get_text(strip=True)

    # Extract detailed summaries with timestamps for the table
    detailed_summaries = []
    for li in soup.find_all('li'):
        timestamp = li.find('strong').get_text(strip=True) if li.find('strong') else ""
        summary_text = li.get_text(strip=True).replace(timestamp, "").strip()
        detailed_summaries.append({'Timestamp': timestamp, 'Summary': summary_text})

    # Convert detailed summaries to DataFrame
    df = pd.DataFrame(detailed_summaries)

    return overall_summary, df

# Streamlit app setup
st.title("YouTube Video Summarizer")
youtube_url = st.text_input("Enter the YouTube video URL:")

if youtube_url:
    # Fetch summarized content
    overall_summary, detailed_summary_df = get_summarized_content(youtube_url)
    
    # Display the overall summary
    st.subheader("Overall Summary")
    st.write(overall_summary)
    
    # Display the detailed summaries with filterable timestamp
    st.subheader("Detailed Summaries")
    timestamp_filter = st.selectbox("Filter by Timestamp", ["All"] + list(detailed_summary_df['Timestamp'].unique()))
    
    if timestamp_filter != "All":
        filtered_df = detailed_summary_df[detailed_summary_df['Timestamp'] == timestamp_filter]
    else:
        filtered_df = detailed_summary_df

    st.dataframe(filtered_df)

    # Optional: Allow downloading of the detailed summaries
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Detailed Summary as CSV",
        data=csv,
        file_name="detailed_summary.csv",
        mime="text/csv"
    )
