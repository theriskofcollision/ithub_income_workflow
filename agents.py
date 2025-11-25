import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()


import google.generativeai as genai

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.llm_api_key = os.getenv("GEMINI_API_KEY")
        if self.llm_api_key:
            genai.configure(api_key=self.llm_api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None

    def log(self, message):
        print(f"[{self.name}] {message}")

    def call_llm(self, prompt):
        if not self.model:
            self.log("WARNING: No LLM API Key found. Returning mock response.")
            return "Mock LLM Response: Analysis complete."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self.log(f"Error calling LLM: {e}")
            return f"Error generating response: {e}"

class TrendScout(Agent):
    def __init__(self):
        super().__init__("TrendScout", "Explorer")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.headers = {"Authorization": f"token {self.github_token}"} if self.github_token else {}

    def search_github(self, query, min_stars=100, limit=5):
        self.log(f"Searching GitHub for: {query}")
        url = "https://api.github.com/search/repositories"
        params = {
            "q": f"{query} stars:>{min_stars}",
            "sort": "stars",
            "order": "desc",
            "per_page": limit
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("items", [])
        else:
            self.log(f"Error searching GitHub: {response.status_code} - {response.text}")
            return []

    def scout(self):
        # Search for Agentic Frameworks, E-commerce, and SaaS starters
        queries = [
            "topic:agentic-ai",
            "topic:ecommerce-plugin",
            "topic:saas-starter-kit",
            "topic:mcp-server",
            "topic:headless-commerce"
        ]
        
        candidates = []
        for q in queries:
            results = self.search_github(q, limit=3)
            candidates.extend(results)
            time.sleep(1) # Rate limit politeness
        
        # Deduplicate
        unique_candidates = {c['html_url']: c for c in candidates}.values()
        self.log(f"Found {len(unique_candidates)} unique candidates.")
        return list(unique_candidates)

class OpportunityAnalyst(Agent):
    def __init__(self):
        super().__init__("OpportunityAnalyst", "Evaluator")

    def analyze(self, repo):
        self.log(f"Analyzing {repo['full_name']}...")
        
        # Get README content
        readme_url = repo['url'] + "/readme"
        # Note: In a real run, we'd fetch the README content via API
        # response = requests.get(readme_url, headers=...)
        # content = base64.b64decode(response.json()['content']).decode('utf-8')
        
        # For this MVP, we'll use the description and topics
        description = repo.get('description', 'No description')
        topics = repo.get('topics', [])
        license_info = repo.get('license', {})
        license_key = license_info.get('key', 'unknown') if license_info else 'unknown'
        
        # Heuristic Analysis
        score = 0
        commercial_licenses = ['mit', 'apache-2.0', 'bsd-3-clause']
        if license_key in commercial_licenses:
            score += 5
        
        if 'agent' in topics or 'ecommerce' in topics:
            score += 3
            
        analysis_prompt = f"""
        Analyze this GitHub repository for monetization potential:
        Name: {repo['full_name']}
        Description: {description}
        Topics: {topics}
        License: {license_key}
        
        Assess:
        1. Problem Solved
        2. Ease of Deployment
        3. Agent Economy Fit
        """
        llm_analysis = self.call_llm(analysis_prompt)
        
        return {
            "repo": repo['full_name'],
            "url": repo['html_url'],
            "score": score,
            "license": license_key,
            "llm_analysis": llm_analysis
        }

class BizDevBot(Agent):
    def __init__(self):
        super().__init__("BizDevBot", "Strategist")

    def create_strategy(self, analysis):
        self.log(f"Creating strategy for {analysis['repo']}...")
        
        strategy_prompt = f"""
        Create a business model for this repository:
        Repo: {analysis['repo']}
        Analysis: {analysis['llm_analysis']}
        
        Propose strategies for:
        1. SaaS Deployment
        2. Paid Plugin/Extension
        3. Agent Service (API)
        """
        strategy = self.call_llm(strategy_prompt)
        
        return {
            "repo": analysis['repo'],
            "url": analysis['url'],
            "strategy": strategy
        }

if __name__ == "__main__":
    # Test run
    scout = TrendScout()
    results = scout.search_github("topic:agentic-ai", limit=1)
    print(f"Test Result: {len(results)} repos found.")
