import csv
import pandas as pd
import psycopg2
import random

df = pd.read_csv("/home/cho/Desktop/workspace/score.csv")

socore = df["steps_window_12"] > 0.0
anomaly = df["anomaly"] ==-1
result = df[socore & anomaly]


conn = psycopg2.connect(
   database="postgres", user='postgres', password='7452', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

cursor = conn.cursor()

print(result)

j = 0 
for i in result["index"]:
    a = random.randint(100,200) 
    j = j + 1 
    cursor.execute(f'''INSERT INTO anomaly_list(index, time,rate) VALUES ({j},'{i}',{a})''')


conn.commit()
print("Records inserted........")

conn.close()

