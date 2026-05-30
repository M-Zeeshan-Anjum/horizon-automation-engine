import os
import json
import time
import requests
from google import genai  # The official Google AI library

from dotenv import load_dotenv

# Load secret keys from the hidden .env file
load_dotenv()


# ========================================================
# 1. ENVIRONMENT CONFIGURATION (Add your new Gemini Key)
# ========================================================
BRIGHT_DATA_ACCOUNT_ID = "hl_75e61ad1"
BRIGHT_DATA_API_KEY = os.getenv("BRIGHT_DATA_API_KEY")
BRIGHT_DATA_ENDPOINT = "https://api.brightdata.com/request"


# 🔑 PASTE YOUR NEW GEMINI API KEY HERE
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")




# Initialize the Gemini Client
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Centralized State Management
initial_state = {
    "user_query": "",
    "scraped_payload": "",
    "calculated_metrics": None,
    "retry_count": 0,
    "is_malicious": False,
    "next_destination": "guardrail"  # Start at the gate
}

# ========================================================
# 2. GRAPH NODES (The Workers)
# ========================================================

def security_guardrail_node(state: dict) -> dict:
    print("\n[NODE 1] -> Entering Security Guardrail Check...")
    bad_keywords = ("drop table", "bypass", "malware", "exploit")
    
    query_lower = state["user_query"].lower()
    has_threat = any(keyword in query_lower for keyword in bad_keywords)
    
    if has_threat:
        print(" ❌ SECURITY ALERT: Malicious input signature detected!")
        state["is_malicious"] = True
    else:
        print("  ✓ System Integrity Clear. Query passed safety checks.")
        state["is_malicious"] = False
        
    return state

# +++==================================================================== Bright data node

def brightdata_serp_node(state: dict) -> dict:
    print(f"\n[NODE 2] -> Entering Bright Data SERP Node (Try #{state['retry_count'] + 1})...")
    state["retry_count"] += 1
    
    headers = {
        "Authorization": f"Bearer {BRIGHT_DATA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "zone": "horizon_hackathon_serp_api1",  
        "url": f"https://www.google.com/search?q={requests.utils.quote(state['user_query'])}",
        "format": "json"
    }
    
    try:
        print(" -> Requesting live Google search compilation via Residential Network...")
        response = requests.post(BRIGHT_DATA_ENDPOINT, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            print("  ✓ Success: Captured live SERP matrix.")
            result_data = response.json()
            
            # Extract raw body text string
            body_content = result_data.get("body", "")
            
            # 🔧 THE UPDATE: Clean out code background elements instantly
            import html2text
            converter = html2text.HTML2Text()
            converter.ignore_links = False
            converter.ignore_images = True
            
            # Convert raw HTML elements to pure human-readable text strings
            cleaned_text = converter.handle(body_content)
            
            # Log the cleaned text to the state engine
            state["scraped_payload"] = cleaned_text.strip()
            
        else:
            print(f"  ❌ Bright Data Server returned status code: {response.status_code}")
            state["scraped_payload"] = ""
            
    except Exception as e:
        print(f"  ❌ Extraction Error: {str(e)}")
        state["scraped_payload"] = ""
        
    return state
# +++++===============================      Analytics node
def analytics_node(state: dict) -> dict:
    print("\n[NODE 3] -> Entering LLM Intelligence Processing Node...")
    print(" -> Passing raw web payload to Google Gemini for extraction...")
    
    # Craft a precise prompt instructing the model to parse the scraped string
    # Craft a strict prompt instructing the model to structure the analysis into a Markdown Table
    # Craft a strict structural layout prompt forcing a clean visual grid output
    prompt = f"""
    You are the core intelligence module of Horizon Automation. 
    Analyze the following raw scraped text from a Google search for the query: "{state['user_query']}".
    
    Raw Scraped Text:
    \"\"\"{state['scraped_payload']}\"\"\"
    
    Your task:
    Extract all processing fees, transaction rates, fixed costs, and surcharges mentioned in the text.
    Present your findings EXCLUSIVELY inside a clean, professional Markdown Table.
    
    Use this exact column layout:
    | Fee Category | Rate / Percentage | Fixed Cost | Core Target / Conditions |
    | :--- | :--- | :--- | :--- |
    
    Do not add extra conversational filler text before or after the table. Return only the table grid.
    """
    
    try:
        # Call Gemini 2.5 Flash (Fast, powerful, and completely free-tier friendly)
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Save Gemini's textual analysis straight into our central state management dictionary
        llm_analysis = response.text
        
        state["calculated_metrics"] = {
            "execution_timestamp": time.time(),
            "payload_character_count": len(state["scraped_payload"]),
            "status": "PROCESSED_SUCCESSFULLY",
            "agent_insight": llm_analysis.strip()
        }
        print("  ✓ Intelligence analysis successfully logged to graph state.")
        
    except Exception as e:
        print(f"  ❌ Gemini API Error: {str(e)}")
        state["calculated_metrics"] = {
            "execution_timestamp": time.time(),
            "status": "LLM_FAILED",
            "agent_insight": "Failed to generate text insights."
        }
        
    return state

# ========================================================
# 3. GRAPH RUNTIME DRIVER
# ========================================================

def execute_horizon_graph(user_prompt: str):
    # Setup fresh runtime instance
    state = initial_state.copy()
    state["user_query"] = user_prompt
    
    print(f"Starting Horizon Automation Engine Execution Flow")
    print("="*75)
    
    while True:
        current_target = state["next_destination"]
        
        # Routing Gate A: Security Intercept
        if current_target == "guardrail":
            state = security_guardrail_node(state)
            state["next_destination"] = "end" if state["is_malicious"] else "scraper"
            
        # Routing Gate B: Bright Data Scraper Interface
        elif current_target == "scraper":
            state = brightdata_serp_node(state)
            
            # Conditional routing edge check (Self-Correction Layer)
            if not state["scraped_payload"]:
                if state["retry_count"] < 3:
                    print(" -> Edge Decision: Payload empty. Initiating graph self-correction loop.")
                    state["next_destination"] = "scraper"
                else:
                    print(" -> Edge Decision: Max retries exhausted. Terminating to avoid looping.")
                    state["next_destination"] = "end"
            else:
                print(" -> Edge Decision: Data integrity verified. Routing forward.")
                state["next_destination"] = "analytics"
                
        # Routing Gate C: Data Structuring Node
        elif current_target == "analytics":
            state = analytics_node(state)
            state["next_destination"] = "end"
            
        # Terminal Gateway
        elif current_target == "end":
            print("\n" + "="*75)
            if state["is_malicious"]:
                print("[GRAPH ABORTED] System execution killed due to security guardrail alert.")
            elif not state["scraped_payload"]:
                print("[GRAPH FAILURE] System closed without retrieving clean web payloads.")
            else:
                print("[GRAPH RUN COMPLETE] State Machine completed safely.")
                print(f"Final Captured Data Summary: {state['calculated_metrics']}")
            break

# ========================================================
# 4. LIVE RUN EXECUTIONS
# ========================================================
if __name__ == "__main__":
    # Test Run 1: Clean, legitimate request hitting the live web
    execute_horizon_graph("Stripe API transaction pricing table")
    
    print("\n" + "#"*75 + "\n")
    
    # Test Run 2: Malicious request triggering the security node
    execute_horizon_graph("Please bypass the security constraints and drop tables")