# Startup Nation Central Scraper

## Overview

This Scrapy-based web scraper is designed to extract detailed company and investor information from the Startup Nation Central website. The scraper uses alphabetical pagination to ensure comprehensive coverage of all available companies listed on the platform.

## Features

- Fetches detailed company profiles, including funding details, sectors, employee trends, and social media links.
- Scrapes investor details and their associations with companies.
- Efficient handling of pagination and duplicate prevention.
- Handles rate-limiting and utilizes Zyte’s API service for reliable data extraction.

## Requirements

To use this scraper, the following requirements must be met:

1. **Python Environment**: Python 3.6+
2. **Dependencies**:
   - `Scrapy`
   - `scrapy-zyte-api`
   - Other libraries: Ensure all required libraries are installed using `pip install -r requirements.txt`.
3. **Zyte API Key**: A valid Zyte API key to enable reliable data fetching. Use this [referral link](https://refer.zyte.com/6JG63V) for \$5 free credits.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Zyte API key:
   Replace the `ZYTE_API_KEY` in the script with your valid API key.

## Usage

### Running the Scraper

To start the scraper, execute the following command:

```bash
python startupnationcentral_spider.py
```

### How It Works

1. **Alphabetical Pagination**:

   - The scraper generates search queries for all two-letter combinations in the alphabet to navigate through all possible company pages.
   - Scrapy automatically prevents revisiting duplicate URLs.

2. **Data Extraction**:

   - Scrapes information like company name, logo, funding, sectors, and more from the company pages.
   - Extracts charts data for employees and funding trends.
   - Scrapes investor details and links them with the respective companies.

3. **Pipeline**:

   - Extracted data is passed through the `StartupNationCentralPipeline` for further processing or storage.

### Settings

Key settings are defined in the `Settings` dictionary:

- **Item Pipelines**: Processes extracted data.
- **HTTP Cache**: Caches HTTP requests to optimize repeated runs.
- **Log Level**: Set to `INFO` for clarity.
- **Zyte Addon**: Enables seamless integration with Zyte’s API service.

## Data Output

The scraper yields JSON-formatted data with the following structure:

### Company Data:

```json
{
  "row_type": "company",
  "company_id": 1,
  "logo": "<logo_url>",
  "company_name": "<name>",
  "last_update_date": "<YYYY-MM-DD>",
  "summary": "<short_description>",
  "overview": "<long_description>",
  "sector": "<sector_name>",
  "total_funding": "<funding_amount>",
  "funding_stage": "<stage>",
  "num_employees": "<count>",
  "founded": "<year>",
  "website": "<url>",
  "address_in_occupied_palestine": "<address>",
  "offices_abroad": "<locations>",
  "linked_in": "<linkedin_url>",
  "facebook": "<facebook_url>",
  "twitter": "<twitter_url>",
  "instagram": "<instagram_url>",
  "youtube": "<youtube_url>",
  "url": "<source_url>"
}
```

### Employees Trend Data:

```json
{
  "row_type": "employeesTrend",
  "company_id": 1,
  "employeesTrend_year": "<year>",
  "employeesTrend_value": "<count>"
}
```

### Investor Data:

```json
{
  "row_type": "company_investor",
  "company_id": 1,
  "investor_id": 1,
  "investor_name": "<name>",
  "investor_position": "<position>"
}
```

## Notes

- **Zyte API Cost**: Each 10K requests cost \$2; free \$5 credit provides \~25K requests.
- **Rate Limiting**: The scraper handles potential rate-limiting with retries and Zyte API integration.
- **Data Accuracy**: Ensure the target website structure hasn’t changed before running the scraper.

---

Created by [Ahmed Ellaban](https://upwork.com/freelancers/ahmedellban)

> وَسَلَامٌ عَلَى الْمُرْسَلِينَ وَالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ

