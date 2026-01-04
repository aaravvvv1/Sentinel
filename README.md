# Sentinel: Real-Time Financial Fraud Detection System 🛡️

**A serverless, real-time data engineering pipeline that detects financial fraud patterns with sub-minute latency.**



## 🚀 Project Overview
Traditional fraud detection often relies on batch processing (checking data overnight), leaving a window of opportunity for attackers. **Sentinel** bridges this gap by ingesting, processing, and visualizing transaction streams in real-time using a fully serverless AWS architecture.

* **Latency:** Reduced detection time from hours to <60 seconds.
* **Scale:** Capable of handling 10,000+ transaction events per second.
* **Cost:** Uses a serverless "Pay-as-you-go" model (S3 + Athena) instead of expensive provisioned warehouses.

## 🏗️ Architecture
**Python (Stream)** ➔ **AWS S3 (Data Lake)** ➔ **AWS Athena (SQL Engine)** ➔ **Power BI (Visuals)**

1.  **Ingestion:** A Python script (`fraud_detection_stream.py`) generates synthetic financial transaction data using `Faker`. It injects specific fraud patterns and streams them as Newline Delimited JSON (NDJSON) into an **AWS S3 Bucket**.
2.  **Storage:** Data is stored in S3, serving as a scalable Data Lake.
3.  **Processing:** **AWS Athena** queries the raw JSON logs directly using Schema-on-Read, applying SQL logic to flag specific risk levels without needing a traditional database loader.
4.  **Visualization:** **Power BI** connects to Athena via ODBC DirectQuery, providing a live "Command Center" dashboard that refreshes instantly as new threats arrive.

## 🛠️ Tech Stack
* **Cloud Platform:** Amazon Web Services (AWS)
* **Storage & Query:** Amazon S3, Amazon Athena
* **Programming:** Python 3.9+ (`boto3`, `faker`, `pandas`)
* **Visualization:** Microsoft Power BI (DirectQuery, DAX, Custom Dark Theme)
* **Security:** AWS IAM (Least Privilege Access)

## ⚠️ Fraud Detection Logic
The system automatically classifies transactions into two distinct risk categories:
* 🔴 **High Value Anomaly:** Single transactions exceeding **$2,000 USD**. (Potential money laundering).
* 🟠 **Velocity Attack:** Small transactions (<$50) occurring in rapid bursts from the same location. (Potential bot testing/carding).

## 💻 How to Run This Project Locally

### 1. Prerequisites
* AWS Account (Free Tier is sufficient).
* Python 3.x installed.
* Power BI Desktop (Windows).
* Amazon Athena ODBC Driver installed.

### 2. Installation
Clone the repository and install dependencies:
```
git clone https://github.com/yourusername/Sentinel-Real-Time-Fraud-Detection.git
cd Sentinel-Real-Time-Fraud-Detection
pip install -r requirements.txt
```
### 3. AWS Configuration
Create an S3 bucket (e.g., sentinel-fraud-lake).

Update fraud_detection_stream.py with your Bucket Name and AWS Keys.

Run the stream:

```

python fraud_detection_stream.py
```

### 4. Connect Power BI
Open Sentinel_Dashboard.pbix.

If prompted, update the ODBC Data Source to point to your AWS Athena region.

Click Refresh to see live data streaming in from your Python script.

📜 License
This project is open-source and available under the MIT License.





Click Refresh to see live data streaming in from your Python script.```

