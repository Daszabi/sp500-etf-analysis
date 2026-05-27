# S&P 500 ETF Performance & Volatility Analysis
This repository contains a Python and SQL-based data pipeline designed to analyze the performance of BlackRock's iShares S&P 500 ETF (IVV).

## Core Features (V1.0)
Automated Data Extraction: Pulls 5-year historical financial data using the yfinance API.
Relational Database Integration: Stores and queries raw financial data using a local SQLite database.
Quantitative Analysis: Uses pandas to calculate 50-day and 200-day moving averages.
Data Visualization: Generates trend and volatility charts using matplotlib.

Note: The source code (etf_analysis.py) is fully functional. Further predictive modeling features are currently being implemented.
