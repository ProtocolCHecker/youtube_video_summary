import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Streamlit UI to get the YouTube URL from the user
st.title("YouTube Video Summarizer")
video_url = st.text_input("Enter the YouTube video URL:")

def get_resume_video(url):
    
    # Setup Chrome WebDriver with headless option
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    
    # driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome()

    # Setup Chrome options for headless execution
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Use webdriver-manager to automatically manage ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the website
    driver.get("https://www.summarize.tech/")

    # XPaths
    url_input_xpath = "/html/body/div/div[1]/div/form/div/input"
    submit_button_xpath = "/html/body/div/div[1]/div/form/div/button"
    see_more_button_1_xpath = "/html/body/div/div[1]/div/section[1]/button"
    see_more_button_2_xpath = "/html/body/div/div[1]/div/section[2]/button"
    
    # Base XPath for the summaries in section 1 and section 2
    resume_base_xpath_1 = "/html/body/div/div[1]/div/section[1]/ul/li[{}]"
    resume_base_xpath_2 = "/html/body/div/div[1]/div/section[2]/ul/li[{}]"

    # Overall summary XPaths
    overall_summary_xpath_1 = "/html/body/div/div[1]/div/section[1]/p"
    overall_summary_xpath_2 = "/html/body/div/div[1]/div/section[2]/p"

    # Enter YouTube URL
    youtube_url = url
    driver.find_element(By.XPATH, url_input_xpath).send_keys(youtube_url)

    # Click the Submit button
    driver.find_element(By.XPATH, submit_button_xpath).click()

    # Wait for the summary to generate
    time.sleep(2)

    # Click both 'See More' buttons before collecting resumes
    for section_xpath in [see_more_button_1_xpath, see_more_button_2_xpath]:
        try:
            driver.find_element(By.XPATH, section_xpath).click()
            time.sleep(2)  # Let the content load after clicking each button
        except Exception as e:
            print(f"Could not find or click the 'See More' button: {e}")

    # Initialize an empty string for the detailed summaries
    detailed_summaries = []

    # Loop through both sections for detailed summaries
    for resume_base_xpath in [resume_base_xpath_1, resume_base_xpath_2]:
        for i in range(1, 13):
            try:
                current_resume_xpath = resume_base_xpath.format(i)
                resume = driver.find_element(By.XPATH, current_resume_xpath).text
                detailed_summaries.append(resume)  # Append each summary to the list
            except Exception as e:
                print(f"Could not find summary for section {i}: {e}")
                break  # Stop if there are fewer than 12 summaries in the section

    # Retrieve overall summaries
    try:
        overall_summary_1 = driver.find_element(By.XPATH, overall_summary_xpath_1).text
        try:
            overall_summary_2 = driver.find_element(By.XPATH, overall_summary_xpath_2).text
            overall_summaries = overall_summary_1 + " " + overall_summary_2  # If both summaries exist
        except Exception:
            overall_summaries = overall_summary_1  # If only the first summary exists
    except Exception as e:
        print(f"Could not retrieve overall summaries: {e}")
        overall_summaries = "Overall summaries not found."

    return {
        "overall": overall_summaries.strip(),  # Return the overall summaries without trailing spaces
        "detailed": detailed_summaries  # Return the detailed summaries as a list
    }

    # Close the browser
    driver.quit()

def resume_text(text):
    # Set up the Chrome WebDriver (make sure to adjust the path to your chromedriver)
    driver = webdriver.Chrome()

    #Setup Chrome WebDriver with headless option
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    
    # driver = webdriver.Chrome(options=chrome_options)

    # Open the specified website
    driver.get("https://copilot.microsoft.com/")

    # Give time for the page to load
    time.sleep(3)

    # Step 1: Click the "Get Started" button
    get_started_button = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/aside/div[1]/div/div[3]/button")
    get_started_button.click()

    # Wait for the next page to load
    time.sleep(3)

    # Step 2: Enter the name "Thom" in the text area
    name_textarea = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/aside/div[1]/div/div[2]/div/div[1]/div/div/div/div/textarea")
    name_textarea.send_keys("Thom")

    # Wait for the action to complete
    time.sleep(1)

    # Step 3: Click the button after writing the name
    name_submit_button = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/aside/div[1]/div/div[2]/div/div[2]/div/button")
    name_submit_button.click()

    # Wait for the action to complete
    time.sleep(1)

    # Step 3: Click the "Meadow" button
    meadow_button = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/aside/div[1]/div/div[1]/div[3]/div/button[1]")
    meadow_button.click()

    # Wait for the action to complete
    time.sleep(2)

    # Step 4: Click the "Next" button
    next_button = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/aside/div[1]/div/div[2]/button")
    next_button.click()

    # Wait for the next page to load
    time.sleep(3)

    # Step 5: Locate the textarea to write the request
    textarea = driver.find_element(By.XPATH, "/html/body/div/main/div[1]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[1]/div/div/div/div/textarea")

    # Step 6: Send the request
    textarea.send_keys(f"I want you to resume this text in 5 detailed bullet points and nothing more: {text}")
    textarea.send_keys(Keys.ENTER)

    # Give some time for the response to be generated
    time.sleep(20)

    # Step 7: Initialize a list to store the bullet points
    bullet_points = []

    # Step 8: Retrieve the bullet points using the provided XPath and store them in the list
    bullet_points.append(driver.find_element(By.XPATH, "/html/body/div/main/div[3]/div/div/div[2]/div[2]/div[2]/div/ul/li[1]").text)
    #time.sleep(1.5)
    bullet_points.append(driver.find_element(By.XPATH, "/html/body/div/main/div[3]/div/div/div[2]/div[2]/div[2]/div/ul/li[2]").text)
    #time.sleep(1.5)
    bullet_points.append(driver.find_element(By.XPATH, "/html/body/div/main/div[3]/div/div/div[2]/div[2]/div[2]/div/ul/li[3]").text)
    #time.sleep(1.5)
    bullet_points.append(driver.find_element(By.XPATH, "/html/body/div/main/div[3]/div/div/div[2]/div[2]/div[2]/div/ul/li[4]").text)
    #time.sleep(1.5)
    bullet_points.append(driver.find_element(By.XPATH, "/html/body/div/main/div[3]/div/div/div[2]/div[2]/div[2]/div/ul/li[5]").text)


    # Close the browser
    driver.quit()

    return bullet_points

# Main logic to get summaries and display them
if video_url:
    summary = get_resume_video(video_url)
    overall_summary = summary["overall"]

    # Get 5 bullet points summary from the overall summary
    bullet_points_summary = resume_text(overall_summary)

    # Display the bullet points in Streamlit
    st.subheader("Overall Summary - 5 Bullet Points")
    for bullet in bullet_points_summary:
        st.write(f"- {bullet}")
    
    # Displaying the detailed summary in a clickable table
    st.subheader("Detailed Summary")
    detailed_summary_df = pd.DataFrame({
        "Detailed Summaries": summary["detailed"]
    })
    st.dataframe(detailed_summary_df)
    
    # Provide downloadable version of the detailed summary
    detailed_summary_csv = detailed_summary_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Detailed Summary as CSV",
        data=detailed_summary_csv,
        file_name="detailed_summary.csv",
        mime="text/csv"
    )
