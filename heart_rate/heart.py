import json 
import random
import time


while (True):
    generated_heart_rate = random.randint(50,220) 
    # print(generated_heart_rate)
    Heartrate = {
        "Heart rate" : generated_heart_rate
    }
    with open('heart.json','w') as json_file:
        json.dump(Heartrate,json_file)
    time.sleep(4)
