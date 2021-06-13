# MIT_B
## 1. Wear OS
## 2. Thingsboard
## 3. Anomaly Detection
#
### 1. Wear OS
### 1.1 개인정보 동의
### 1.2 MQTT
### 1.3 이상탐지 내역 확인
### 1.4 최근 심박수 그래프화
#
### 2. Thingsboard
### 우분투 20.04LTS

### 2.1 KAFKA
##### # install and launch the zookeeper service:
##### sudo apt-get install zookeeper
##### wget https://archive.apache.org/dist/kafka/2.6.0/kafka_2.13-2.6.0.tgz
##### tar xzf kafka_2.13-2.6.0.tgz
##### sudo mv kafka_2.13-2.6.0 /usr/local/kafka
##### sudo nano /etc/systemd/system/zookeeper.service
##### sudo nano /etc/systemd/system/kafka.service

### 2.2 Postgresql + TimescaleDB
##### # install and launch the postgresql service:
###### sudo apt install -y wget
###### wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
###### RELEASE=$(lsb_release -cs)
###### echo "deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}"-pgdg main | sudo tee  /etc/apt/sources.list.d/pgdg.list
###### # install and launch the postgresql service:
###### sudo apt update
###### sudo apt -y install postgresql-12
###### sudo service postgresql start
##### # install and launch the TimesacleDB service:
###### echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -c -s)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
###### wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
###### sudo apt-get update
###### sudo add-apt-repository ppa:timescale/timescaledb-ppa
###### sudo apt-get update
###### sudo apt install timescaledb-2-postgresql-13

### 2.3 Dashboard

#
### 3. Anomaly Detection
### 3.1 데이터 베이스 연동
### 3.2 필터링
### 3.3 전처리
### 3.4 주기성 보정
### 3.5 이상탐지 
### 3.6 시각화
