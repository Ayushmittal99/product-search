# Amazon Product Research AI Agent

## Overview

An AI-powered product research automation tool that helps users discover Amazon products based on custom criteria such as category, price range, ratings, and reviews.

The application fetches product data using SerpAPI, filters products according to user requirements, and stores results automatically in Google Sheets.

---

## Features

- Amazon product search automation
- Price range filtering
- Rating filtering
- Review count filtering
- Google Sheets integration
- Flask web interface
- Automated data collection and reporting

---

## Tech Stack

- Python
- Flask
- SerpAPI
- Google Sheets API
- HTML
- CSS

---

## Project Workflow

1. User enters search criteria.
2. Flask receives the request.
3. SerpAPI fetches Amazon product data.
4. Products are filtered based on:
   - Price
   - Rating
   - Reviews
5. Results are stored in Google Sheets.
6. Filtered products are displayed to the user.

---

## Example Input

Category: Kitchen

Price Range: $10 - $30

Minimum Reviews: 100

Minimum Rating: 4.0

---

## Example Output

- Product Name
- Price
- Rating
- Review Count
- Product URL

---

requests==2.31.0
flask==3.0.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
google-api-python-client==2.107.0
python-dotenv==1.0.0
