# GitHub Income Workflow

This project implements an agentic workflow to discover, analyze, and strategize income generation opportunities using GitHub Apps and the Agent Economy.

## Components

- **TrendScout:** Searches GitHub for high-potential repositories (Agentic AI, E-commerce, SaaS).
- **OpportunityAnalyst:** Evaluates repositories for monetization potential (License, Demand).
- **BizDevBot:** Generates specific business strategies (SaaS, Plugins, Agent Services).

## How to Run on GitHub

1.  **Fork/Push** this repository to your GitHub account.
2.  **Go to Settings > Secrets and variables > Actions**.
3.  Add the following Repository Secrets:
    - `GEMINI_API_KEY`: Your Google Gemini API Key.
    - `GH_TOKEN`: A GitHub Personal Access Token (optional, for higher rate limits).
4.  **Go to the "Actions" tab**.
5.  Select **"Run GitHub Income Agent"** on the left.
6.  Click **"Run workflow"**.
7.  Once finished, download the `income-report` artifact to see the results.

## Local Setup (Optional)

1.  **Install Dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```

2.  **Environment Variables:**
    Create a `.env` file:
    ```bash
    GITHUB_TOKEN=your_github_token
    GEMINI_API_KEY=your_gemini_api_key
    ```

3.  **Run:**
    ```bash
    python3 workflow.py
    ```
