import json 
import random
import time


while (True):
    generated_heart_rate = random.randint(0,60) 
    # print(generated_heart_rate)
    step = {
        "step" : generated_heart_rate
    }
    with open('step.json','w') as json_file:
        json.dump(step,json_file)
    time.sleep(60)
