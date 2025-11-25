import os
import json
from agents import TrendScout, OpportunityAnalyst, BizDevBot

def run_workflow():
    print("Starting GitHub Income Workflow...")
    print("===================================")
    
    # 1. Initialize Agents
    scout = TrendScout()
    analyst = OpportunityAnalyst()
    bizdev = BizDevBot()
    
    # 2. Scouting Phase
    print("\n--- Phase 1: Scouting ---")
    candidates = scout.scout()
    print(f"Scouted {len(candidates)} candidates.")
    
    # 3. Analysis Phase
    print("\n--- Phase 2: Analysis ---")
    viable_opportunities = []
    for repo in candidates:
        analysis = analyst.analyze(repo)
        if analysis['score'] >= 5: # Filter for high potential
            viable_opportunities.append(analysis)
            print(f"Qualified: {repo['full_name']} (Score: {analysis['score']})")
        else:
            print(f"Disqualified: {repo['full_name']} (Score: {analysis['score']})")
            
    # 4. Strategy Phase
    print("\n--- Phase 3: Strategy Generation ---")
    final_report = []
    for opp in viable_opportunities[:5]: # Limit to top 5 for now
        strategy = bizdev.create_strategy(opp)
        final_report.append(strategy)
        
    # 5. Reporting
    print("\n=== Final Report ===")
    with open("income_report.json", "w") as f:
        json.dump(final_report, f, indent=2)
        
    for item in final_report:
        print(f"\nRepo: {item['repo']}")
        print(f"URL: {item['url']}")
        print(f"Strategy: {item['strategy']}")
        print("-" * 30)
        
    print("\nWorkflow Complete. Report saved to income_report.json")

if __name__ == "__main__":
    run_workflow()
