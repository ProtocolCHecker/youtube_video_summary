import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from bs4 import BeautifulSoup

# Streamlit UI to get the YouTube URL
st.title("YouTube Video Summarizer with Timestamp Filter")
video_url = st.text_input("Enter the YouTube video URL:")

def summarize_video(url):
    # Setup Chrome WebDriver with error handling
    driver = None
    try:
        # Setup Chrome WebDriver with headless option
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        # Initialize Chrome WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        #driver = webdriver.Chrome()

        # Open the summarization website
        driver.get("https://www.summarize.tech/")
        time.sleep(2)  # Allow page to load

        # Input YouTube URL and click submit
        url_input_xpath = "/html/body/div/div[1]/div/form/div/input"
        submit_button_xpath = "/html/body/div/div[1]/div/form/div/button"
        driver.find_element(By.XPATH, url_input_xpath).send_keys(url)
        driver.find_element(By.XPATH, submit_button_xpath).click()
        time.sleep(5)  # Wait for the page to generate the summary

        # Extract content from the current page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #summary_section = soup.find('section')  # Assuming the summary appears within a <section> tag
        time.sleep(5)
        # Concatenate overall summaries starting with "In the 'Bankless'" or "In the 'Announcing'"
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

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "", pd.DataFrame()

    finally:
        # Ensure driver is closed
        if driver:
            driver.quit()

    return overall_summary, df

# Display summary if URL is entered
if video_url:

    overall_summary, detailed_summary_df = summarize_video(video_url)
    
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