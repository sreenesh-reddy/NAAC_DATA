from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import traceback
from rapidfuzz import process,fuzz
import time
import re
import pandas as pd
flag=0
loop=False
driver = webdriver.Chrome()


def find_closest_match_fuzzy(target, options,threshold):
    matches= process.extract(target, options,scorer=fuzz.partial_ratio)
    print('='*20)
    print('TARGET:',target)
    for match, score, _ in matches:
        print(f"Match: {match}, Score: {score}")

    return [(match, score) for match, score, _ in matches if score >= threshold]



def extract_college_name_from_url(url):
    """
    Extracts the college name from a Google Maps URL.
    The name appears as words separated by '+' in the URL path.
    """
    match = re.search(r'/place/([^/]+)/@', url)
    if match:
        college_name = match.group(1).replace('+', ' ')
        return college_name
    return "Unknown College"


def place(college_name):
    try:
        close_feedback_popup()  # Close popup if present before clicking
        zoom_in_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "widget-zoom-in"))
        )

        for _ in range(4):
            # Wait until zoom button is enabled
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "widget-zoom-in")))
            zoom_in_button.click()
        time.sleep(1)  # Pause after each click to let map adjust

    except Exception as e:
        print(f"Zoom-in button issue for {college_name}: {e}")

    # Get map container
    map_container = driver.find_element(By.CLASS_NAME, "widget-scene-canvas")


    # Calculate center point
    center_x = 150
    center_y = 0

    # Right-click at center
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(map_container, center_x, center_y).context_click().perform()
    
    try:
        # Wait for coordinates to appear
        coordinates_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mLuXec"))  # Class for coordinates in right-click menu
        )
        coordinates_text = coordinates_element.text.strip()
        coordinates_list.append(coordinates_text)
        print('SINGLE RESULT COLLEGE COORDINATES:',college_name,coordinates_text)
        return
    except Exception as e:
        coordinates_list.append('')
        print(f"Failed to extract coordinates for {college_name}: {e}")
        print(traceback.format_exc()) 
        driver.quit()
        driver.get("https://www.google.com/maps")
        get_college_names(college_name,0)
        return


def multiple_places(results,college_names,college_name,flag):
    if(flag==0):
        for result in results:                
            result.click()
            time.sleep(1)
            current_url = driver.current_url
            extracted_name = extract_college_name_from_url(current_url)
            if extracted_name and extracted_name not in college_names:
                college_names.append(extracted_name)
    else:
        results[0].click()
        time.sleep(1)
        try:
            zoom_in_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "widget-zoom-in"))
            )

            for _ in range(4):
                # Wait until zoom button is enabled
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "widget-zoom-in")))
                zoom_in_button.click()
            time.sleep(1)  # Pause after each click to let map adjust

        except Exception as e:
            print(f"Zoom-in button issue for {college_name}: {e}")

        time.sleep(1)
        results[1].click()
        time.sleep(1)
        results[0].click()
        time.sleep(1)

        map_container = driver.find_element(By.CLASS_NAME, "widget-scene-canvas")

        center_x = 500
        center_y = 0

        # Right-click at center
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(map_container, center_x, center_y).context_click().perform()
        
        try:
            # Wait for coordinates to appear
            coordinates_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mLuXec"))  # Class for coordinates in right-click menu
            )
            coordinates_text = coordinates_element.text.strip()
            coordinates_list.append(coordinates_text)
            #print('SINGLE RESULT COLLEGE COORDINATES:',college_name,coordinates_text)
            return
        except Exception as e:
            coordinates_list.append('')
            print(f"Failed to extract coordinates for {college_name}: {e}")
            print(traceback.format_exc()) 
            driver.quit()
            driver.get("https://www.google.com/maps")
            get_college_names(college_name,0)
            return


def get_college_names(college_name,flag):
    # Search for the college
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'searchboxinput')))
    search_box.clear()
    search_box.send_keys(college_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(4)  # Wait for results to load

    # Check if multiple results appear
    try:
        #print('='*5)
        college_names = []
        current_url = driver.current_url
        if "place" in current_url:
            place(college_name)
            return
        else:
            #print('Multiple rsults found:',college_name, flag)
            results = driver.find_elements(By.CLASS_NAME, "Nv2PK")
            if(results):
                multiple_places(results,college_names,college_name,flag)
            else:
                coordinates_list.append('')
                return
        return college_names
    except Exception as e:
        print(f"Error handling results: {e}")
        print(traceback.format_exc())  # This will print the full traceback
        coordinates_list.append('')
    return



def close_feedback_popup():
    try:
        # Wait and check if the feedback popup exists
        popup = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "widget-consent-dialog"))
        )
        close_button = popup.find_element(By.TAG_NAME, "button")
        close_button.click()
        print("Closed feedback popup.")
        time.sleep(1)  # Give time for the popup to disappear
    except Exception:
        pass  # If no popup appears, continue normally


# Example usage
def test(target,district,state):
    temp=get_college_names(target+' in '+state+','+district,0)
    if(temp):
        best_matches = find_closest_match_fuzzy(target, temp,20)
        best_matches.sort(key=lambda x: x[1], reverse=True)
        top_match = best_matches[0] if best_matches else []

        if top_match:
            print(top_match[0], type(top_match[0]))
            top=top_match[0]
            top=top.replace('to', '')
            get_college_names(top+' in '+state+','+district,1)
        else:
            print('no matches found in best similarity')
            coordinates_list.append("")
        print('='*20)  
    else:
        pass



coordinates_list = []
driver.get("https://www.google.com/maps")

def main():
    path="part1_part4_data_files/part_"
    for x in range(7,11):
        global coordinates_list
        coordinates_list = []
        df = pd.read_csv(path+str(x)+".csv") 
        for index, row in df.iterrows():

            college_name = row["Name"]
            state=row["State"]
            district = row["District"]

            print('*'*15)
            print('searching for college name:',college_name)
            test(college_name,district,state)
            print('*'*15)


        df["lat,long"] = coordinates_list
        df.to_csv(path+str(x)+".csv", index=False)
        print('data saved sucessfully')


# test('Saraswathi College of Arts & Science, Dachepalli','Guntur')
main()
print(coordinates_list)
driver.quit()
