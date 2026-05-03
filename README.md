# 🚕 NYC Taxi Data Quality Checker & Analytics

An automated data profiling and cleaning tool designed to identify business anomalies and technical errors in the NYC Yellow Taxi dataset. This project combines a robust Python processing pipeline with visual data storytelling.

## 📖 Project Overview
The goal of this project is to automate the Data Quality (DQ) assessment process. It processes millions of taxi trip records to detect logical inconsistencies—such as negative fares, impossible trip distances, or suspicious tip patterns—and generates a professional report for business stakeholders.

## 📊 Dataset
The project uses the **NYC Yellow Taxi Trip Records** dataset.
* **Source:** [DataTalksClub NYC TLC Data (GitHub)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow)
* **Specific File:** `yellow_tripdata_2021-01.csv`
* **Note:** This specific month was chosen to demonstrate data cleaning techniques on a large-scale real-world dataset. Due to file size limits, the CSV is not included in the repository.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas
* **Visualization:** Matplotlib, Seaborn
* **Environment:** Jupyter Notebook, VS Code

## 📂 Project Structure
```text
data-quality-checker/
│
├── data/                    # Raw dataset (CSV)
├── output/                  # Generated reports (report.txt)
├── main.py                  # Main data quality engine
├── taxi_analysis.ipynb      # Visualization & EDA
└── README.md                # Project documentation

## 🚀 How to Run

1. **Clone the repository:**
    ```bash
    git clone https://github.com/skozica23/data-quality-checker.git
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare the data:**
    * Create a folder named `data/` in the root directory.
    * Download the `yellow_tripdata_2021-01.csv` file from the NYC TLC website and place it inside the `data/` folder.

4. **Run the analysis:**
    * To generate the report: `python main.py`
    * To view visualizations: Open `taxi_analysis.ipynb` in Jupyter or VS Code.