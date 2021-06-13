# MIT_B
## 1. Wear OS
## 2. Thingsboard
## 3. Anomaly Detection
#
### 1. Wear OS
### 1.1 개인정보 동의
###### # install **wget** if not already installed:
sudo apt install -y wget

# import the repository signing key:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# add repository contents to your system:
RELEASE=$(lsb_release -cs)
echo "deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}"-pgdg main | sudo tee  /etc/apt/sources.list.d/pgdg.list

# install and launch the postgresql service:
sudo apt update
sudo apt -y install postgresql-12
sudo service postgresql start
### 1.2 MQTT
### 1.3 이상탐지 내역 확인
### 1.4 최근 심박수 그래프화
#
### 2. Thingsboard
### 우분투 20.04LTS
### 2.1 KAFKA
### 2.2 Dashboard
### 2.3 Postgresql + Timescaledb
#
### 3. Anomaly Detection
### 3.1 데이터 베이스 연동
### 3.2 필터링
### 3.3 전처리
### 3.4 주기성 보정
### 3.5 이상탐지 
### 3.6 시각화
