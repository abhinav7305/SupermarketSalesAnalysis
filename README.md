# Supermarket Sales Analysis

A reproducible exploratory data analysis project for the IBM SkillsBuild Data Analytics with AI Academic Internship Program, conducted by BharatCares in association with AICTE. It turns supermarket transactions into findings about product lines, branches, customer types, payment methods, and ratings.

## Dataset

This project uses the public [Supermarket Sales dataset on Kaggle](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales). Download the CSV named supermarket_sales - Sheet1.csv before running the analysis. The source has 1,000 transactions from three branches in Yangon, Mandalay, and Naypyitaw.

The dataset is not committed to this repository. Download it directly from Kaggle, then put it in the project root or a data folder. This keeps the repository lightweight and attributes the source correctly.

## Project questions

- Which product line generates the highest sales?
- Which branch performs best?
- Which category sells the most?
- What is the most popular payment method?
- Do Members spend more than Normal customers?
- What is the average customer rating?

Sales are calculated as Quantity x Unit price. This is kept separate from the Kaggle Total column, which includes tax.

## Technologies

- Python 3.10+
- pandas for cleaning and aggregation
- matplotlib and seaborn for visualizations

## Run locally

1. Clone the repository and open its folder.
2. Create and activate a virtual environment (recommended).

~~~powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
~~~

3. Install dependencies.

~~~powershell
pip install -r requirements.txt
~~~

4. Download the Kaggle CSV and run:

~~~powershell
python Abhinav_SupermarketSalesAnalysis.py --data "C:\\path\\to\\supermarket_sales - Sheet1.csv"
~~~

Alternatively, place the file at data/supermarket_sales - Sheet1.csv and run:

~~~powershell
python Abhinav_SupermarketSalesAnalysis.py
~~~

5. Review terminal findings and the generated outputs folder. It contains four charts, four CSV summary tables, a data-quality summary, and a text result summary.

## Repository structure

~~~text
.
├── Abhinav_SupermarketSalesAnalysis.py
├── Abhinav_ProjectReport.docx
├── README.md
└── requirements.txt
~~~

Generated outputs and the downloaded dataset are excluded from the source submission. Add them to .gitignore if you decide to keep them locally.

## Business use

The analysis helps prioritize inventory for high-revenue product lines, investigate the strongest branch’s practices, maintain convenient payment choices, and target membership or customer-service improvements using observed spending and ratings. All findings are calculated at runtime, so they remain correct if the dataset is updated.

