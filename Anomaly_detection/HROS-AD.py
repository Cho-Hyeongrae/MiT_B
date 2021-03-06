import warnings
warnings.filterwarnings('ignore')
import sys 
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import psycopg2
import csv
#%matplotlib inline
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.preprocessing import StandardScaler
from sklearn.covariance import EllipticEnvelope
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM

####################################

parser = argparse.ArgumentParser(description='Find anomalies in wearables time-series data.')
parser.add_argument('--heart_rate', metavar='', help ='raw heart rate count with a header = heartrate')
parser.add_argument('--steps',metavar='', help ='raw steps count with a header = steps')
parser.add_argument('--myphd_id',metavar='', default = 'myphd_id', help ='user myphd_id')
parser.add_argument('--figure', metavar='',  default = 'myphd_id_anomalies.pdf', help='save predicted anomalies as a PDF file')
parser.add_argument('--anomalies', metavar='', default = 'myphd_id_anomalies.csv', help='save predicted anomalies as a CSV file')
parser.add_argument('--symptom_date', metavar='', default = 'NaN', help = 'symptom date with y-m-d format')
parser.add_argument('--diagnosis_date', metavar='', default = 'NaN',  help='diagnosis date with y-m-d format')
parser.add_argument('--outliers_fraction', metavar='', type=float, default=0.1, help='fraction of outliers or anomalies')
parser.add_argument('--random_seed', metavar='', type=int, default=10, help='random seed')
args = parser.parse_args()

# as arguments
fitbit_oldProtocol_hr = args.heart_rate
fitbit_oldProtocol_steps = args.steps
myphd_id = args.myphd_id
myphd_id_figure = args.figure
myphd_id_anomalies = args.anomalies
symptom_date = args.symptom_date
diagnosis_date = args.diagnosis_date
RANDOM_SEED = args.random_seed
outliers_fraction =  args.outliers_fraction

###################################

class HROSAD_offline:
    #????????? ??????
    def HROS(self, heartrate, steps):   
         # HROS??? ????????? ??? ????????? ???????????? ???????????? ????????? ???????????? ???????????????. 
        
        
        #connect DB
        conn = psycopg2.connect(host="localhost", port = 5432, 
        database="postgres", user="postgres", password="7452")
        cur1 = conn.cursor()
        cur1.execute("""SELECT * FROM heartrate""")
        query_results_hr = cur1.fetchall()
        
        cur2 = conn.cursor()
        cur2.execute("""SELECT * FROM steps""")
        query_results_stpes = cur2.fetchall()
        cur1.close()
        cur2.close()
        conn.close()
        with open('team2_hr.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in query_results_hr:
                writer.writerow(row)
                
        with open('team2_steps.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in query_results_stpes:
                writer.writerow(row)
        # heart rate data
        df_hr = pd.read_csv("path_csv")
        df_hr = df_hr.set_index('datetime')
        df_hr.index.name = None
        df_hr.index = pd.to_datetime(df_hr.index)

        # steps data
        df_steps = pd.read_csv("path_csv")
        df_steps = df_steps.set_index('datetime')
        df_steps.index.name = None
        df_steps.index = pd.to_datetime(df_steps.index)
        df_steps["steps"] = df_steps["steps"].apply(lambda x: x + 1) # 0?????? ????????? ???????????? ?????? ?????? ?????? +1??? ?????????.

        # merge dataframes
        df1 = pd.merge(df_hr, df_steps, left_index=True, right_index=True) #?????? ???,??????,???,??? ???????????? ??????????????? csv ??????
        df1['heartrate'] = (df1['heartrate']/df1['steps'])  # ????????? ????????? = ?????????/?????????
        return df1


    def pre_processing(self, resting_heart_rate):
        # ????????? ????????????????????? ????????????(moving averages) 400 
        # ?????? ???????????? 1???????????? ?????? ???????????? ??????????????????.

        df_nonas = df1.dropna()
        df1_rom = df_nonas.rolling(400).mean() #?????? ??????
      
        df2 = df1_rom.resample('10min').mean() #  ?????? ?????????
        df2 = df2.dropna()
        return df2

    # ????????? ?????? ??????
    def seasonality_correction(self, heartrate, steps):
        # ???????????? ?????? ???????????? ???????????? ???????????????.

        # ?????????, ????????? ???????????? additive????????? ???????????? trend + resid?????? ????????? ????????? 1??? ?????? ????????? ?????????.
        sdHR_decomposition = seasonal_decompose(sdHR, model='additive', freq=1)
        sdSteps_decomposition = seasonal_decompose(sdSteps, model='additive', freq=1)
        sdHR_decomp = pd.DataFrame(sdHR_decomposition.resid + sdHR_decomposition.trend)
        sdHR_decomp.rename(columns={sdHR_decomp.columns[0]:'heartrate'}, inplace=True)
        sdSteps_decomp = pd.DataFrame(sdSteps_decomposition.resid + sdSteps_decomposition.trend)
        sdSteps_decomp.rename(columns={sdSteps_decomp.columns[0]:'steps_window_12'}, inplace=True)
        frames = [sdHR_decomp, sdSteps_decomp]
        data = pd.concat(frames, axis=1)
        return data


    # ????????? ??????
    def standardization(self, seasonality_corrected_data):
        # ???????????? ?????? ???????????? 0, ????????? 1??? ????????????(Z??????)?????? ???????????? ????????? ?????????. 
        data_scaled = StandardScaler().fit_transform(data_seasnCorec.values)
        data_scaled_features = pd.DataFrame(data_scaled, index=data_seasnCorec.index, columns=data_seasnCorec.columns)
        data_df = pd.DataFrame(data_scaled_features)
        data = pd.DataFrame(data_df).fillna(0)
        data.to_csv('data.csv')
        return data
    
    # ?????? ?????? ??? ???????????? ??????
    def anomaly_detection(self, standardized_data):
        # ???????????? ???????????? ???????????? OC-SVM??? ???????????? ???????????? ?????? ?????????.
        # ????????? ???????????? 1??? ?????? -1??? ??????????????? ???????????????.
        model =  EllipticEnvelope(contamination=outliers_fraction, 
                             #behaviour="new",
                             random_state=RANDOM_SEED, support_fraction=0.7)



        model.fit(std_data)

        preds = pd.DataFrame(model.predict(std_data))
        preds = preds.rename(lambda x: 'anomaly' if x == 0 else x, axis=1)
        data = std_data.reset_index()
        data = data.join(preds)
        data.to_csv('score.csv')
        return data

    # ?????????
    def visualize(self, results, symptom_date, diagnosis_date, user):
        #????????? csv??????, PNG????????? ??????

        try:

            with plt.style.context('fivethirtyeight'):
                fig, ax = plt.subplots(1, figsize=(80,15))
                a = data.loc[data['anomaly'] == -1, ('index', 'heartrate')] #anomaly
                b = a[(a['heartrate']> 0)]
                ax.bar(data['index'], data['heartrate'], linestyle='-',color='midnightblue' ,lw=6, width=0.01)
                ax.scatter(b['index'],b['heartrate'], color='red', label='Anomaly', s=500)
                # We change the fontsize of minor ticks label
                ax.tick_params(axis='both', which='major', color='blue', labelsize=60)
                ax.tick_params(axis='both', which='minor', color='blue', labelsize=60)
                ax.set_title(myphd_id,fontweight="bold", size=50) # Title
                ax.set_ylabel('Std. HROS\n', fontsize = 50) # Y label
                ax.axvline(pd.to_datetime(symptom_date), color='red', zorder=1, linestyle='--', lw=8) # Symptom date 
                ax.axvline(pd.to_datetime(diagnosis_date), color='purple',zorder=1, linestyle='--', lw=8) # Diagnosis date
                ax.tick_params(axis='both', which='major', labelsize=60)
                ax.tick_params(axis='both', which='minor', labelsize=60)
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
                #ax.tick_params(labelrotation=90,fontsize=14)
                ax.grid(zorder=0)
                ax.grid(True)
                #plt.legend()
                plt.xticks(fontsize=30, rotation=90)
                plt.yticks(fontsize=50)
                ax.patch.set_facecolor('white')
                fig.patch.set_facecolor('white')
                plt.show()
                figure = fig.savefig(myphd_id_figure, bbox_inches='tight')  
                # Anomaly results
                b['Anomalies'] = myphd_id
                b.to_csv(myphd_id_anomalies, mode='a', header=False)        
                return figure

        except:
            with plt.style.context('fivethirtyeight'):
                fig, ax = plt.subplots(1, figsize=(80,15))
                a = data.loc[data['anomaly'] == -1, ('index', 'heartrate')] #anomaly
                b = a[(a['heartrate']> 0)]
                ax.bar(data['index'], data['heartrate'], linestyle='-',color='midnightblue' ,lw=6, width=0.01)
                ax.scatter(b['index'],b['heartrate'], color='red', label='Anomaly', s=1000)
                ax.tick_params(axis='both', which='major', color='blue', labelsize=60)
                ax.tick_params(axis='both', which='minor', color='blue', labelsize=60)
                ax.set_title(myphd_id,fontweight="bold", size=50) # Title
                ax.set_ylabel('Std. HROS\n', fontsize = 50) # Y label
                #ax.axvline(pd.to_datetime(symptom_date), color='red', zorder=1, linestyle='--', lw=8) # Symptom date 
                #ax.axvline(pd.to_datetime(diagnosis_date), color='purple',zorder=1, linestyle='--', lw=8) # Diagnosis date 
                ax.tick_params(axis='both', which='major', labelsize=60)
                ax.tick_params(axis='both', which='minor', labelsize=60)
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
                ax.grid(zorder=0)
                ax.grid(True)
                plt.xticks(fontsize=30, rotation=90)
                plt.yticks(fontsize=50)
                ax.patch.set_facecolor('white')
                fig.patch.set_facecolor('white')     
                figure = fig.savefig(myphd_id_figure, bbox_inches='tight')  
                # Anomaly results
                b['Anomalies'] = myphd_id
                b.to_csv(myphd_id_anomalies, mode='a', header=False)        
                return figure


model = HROSAD_offline()

df1 = model.HROS(fitbit_oldProtocol_hr, fitbit_oldProtocol_steps)
df2 = model.pre_processing(df1)
sdHR = df2[['heartrate']]
sdSteps = df2[['steps']]
data_seasnCorec = model.seasonality_correction(sdHR, sdSteps)
data_seasnCorec += 0.1
std_data = model.standardization(data_seasnCorec)
data = model.anomaly_detection(std_data)
model.visualize(data, symptom_date, diagnosis_date)
