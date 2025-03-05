from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import traceback

import time
import re
flag=0
loop=False

# Setup Selenium WebDriver
driver = webdriver.Chrome()

def find_closest_match_fuzzy(target, options,threshold):
    matches= process.extract(target, options,scorer=fuzz.partial_ratio)
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

def get_college_names(college_name,flag):
    """
    Searches for a college on Google Maps and extracts the college names from the results.
    """
    # Open Google Maps
    
    # Search for the college
    search_box = driver.find_element(By.NAME, "q")
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
            #print("Single result (directly opened)")
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
                #print('SINGLE RESULT COLLEGE COORDINATES:',college_name,coordinates_text)
                return
            except Exception as e:
                coordinates_list.append('')
                print(f"Failed to extract coordinates for {college_name}: {e}")
                return
        else:
            #print('Multiple rsults found:',college_name, flag)
            results = driver.find_elements(By.CLASS_NAME, "Nv2PK")
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
                    return





        print("\n".join(college_names))  # Print extracted names
        return college_names
    except Exception as e:
        print(f"Error handling results: {e}")
        print(traceback.format_exc())  # This will print the full traceback

    return
from rapidfuzz import process,fuzz

# Example usage
def test(target,district):
    temp=get_college_names(target+' in '+district,0)
    # Close the driver
    

    if(temp):
        
        # Example usage
        best_matches = find_closest_match_fuzzy(target, temp,30)

        #print('BEST MATCHES FOUND FOR MULTIPLE RESULT:',best_matches)

        best_matches.sort(key=lambda x: x[1], reverse=True)

            # Always return the top match
        
        top_match = best_matches[0] if best_matches else []

        if top_match:
            # final=[]
            # # Check if there's a second match within the score difference threshold
            # if len(best_matches) > 1 and abs(top_match[1] - best_matches[1][1]) <= 1.5:
            #     final=[top_match[0], best_matches[1][0]] # Return both
            # else:
            #     final=[top_match[0]]  # Return only the top match
            #print('final:',final)
            # for x in final:
            #     get_college_names(x+' in '+district,1)
            get_college_names(top_match[0]+' in '+district,1)
        else:
            print('no matches found in best similarity')
    else:
        pass
        #print('temp found to be empty')



import pandas as pd 

coordinates_list = []
df = pd.read_csv("data2_files/part_8.csv") 
driver.get("https://www.google.com/maps")

for index, row in df.iterrows():

    college_name = row["Name"]
    district = row["District"]

    test(college_name,district)
#test('Zoological Survey of India','Nicobars')
print(coordinates_list)
df["lat,long"] = coordinates_list
driver.quit()
