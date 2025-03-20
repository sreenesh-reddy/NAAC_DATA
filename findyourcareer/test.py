from google import genai
from google.genai import types
import pandas as pd
import numpy as np
import os
api_keys=["AIzaSyDxBnQ-CKHnVDUj69XCmu2ouX9-OyCbD9s","AIzaSyDLx0s0LI3R93PPlDhz1_7RoS5ILrszJKA", "AIzaSyBpbNk3R9br6mDmQeqNkBhFMHYI6PIMGp0","AIzaSyBkxdM0Fv3uGk77bBDQ-EI7UFIZ4bIxxEQ", "AIzaSyA6elRmgHFFWhrw1tVghpd4eWRTY-eImR0","AIzaSyARZdv6cWGnkL99PkAQ9ItlgN1U2J4R7Fw","AIzaSyDskxxa9LftXDM6oSvUTLH-NBXHHpe__sg","AIzaSyAhjg1mVl8csbzf9UMDFPY2w_M3G1uvt7E","AIzaSyAmiV6pFpo6E38fQCvrdn_m1HY-D0BgQB8","AIzaSyD3fwrbbo5c7qgdFPZrt8szJ0M2AqJbzlI","AIzaSyDM7fCF_Yt5vV5Q1hwS4JAZPL-GNMABHpQ"]
client = genai.Client(api_key=api_keys[0])
c=0
i=0
n=len(api_keys)
data=pd.read_csv('findyourcareer.csv')
responses=[]
counter=1

for index,row in data.iterrows():

    if(counter==16):
        counter=1
        if(i+1<n):
            i+=1
        else:
            i=0
            client=genai.Client(api_key=api_keys[i])
    try:
        prompt = f"""
        Write a 300-word description for the course titled "{row['Title']}".
        - **Institute Name**: {row['Institute Name']}
        - **Short Description**: {row['Short Description']}
        - **Mode of Delivery**: {row['mode of study']}
        - **Course Duration in months**: {row['Course Duration']}
        - **Course Fee in Rs**: {row['Course Fee']}
        - **URL**: {row['URL']}
        - **Course Level**: {row['Course Level']}
        - **Eligibility**: {row['Other Eligibility']}
        - **Credential**: {row['Credential']}
        - **Total Fees Total Fees
(<1 L/1-2 L/2-3 L/>3L)**: {row['Total Fees']}
        - **Location**: {row['Location']}
        - **Duration
(<6/6-12/12-24)**: {row['Duration']}
        - **Category**: {row['Category']}

        The description should include an overview of the course, its structure, key topics, and potential career outcomes. Highlight any unique features or benefits of the course.
        """
        response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=500,  # Increased to ensure completion
            temperature=0.7,
        ))

        responses.append(response.text)
        print('counter:',c)
        print(response.text)
        print('='*50)

    except Exception as e:
        responses.append('')
        print('exception occured:',e)
    counter+=1
    c+=1

data['Long Description']= responses
# data.to_csv('findyourcareer.csv')
print("Descriptions generated successfully!")