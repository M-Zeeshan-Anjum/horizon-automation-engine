# webpage made with streamlit

import streamlit as st
import json
import time
from horizon_engine import (
    initial_state, 
    security_guardrail_node, 
    brightdata_serp_node, 
    analytics_node
)

# Set page configuration for a professional look
st.set_page_config(
    page_title="Horizon Automation | Market Intelligence Agent",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for styling the UI components cleanly
st.markdown("""
<style>
    .reportview-container { background: #f0f2f6; }
    .stAlert { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# App Title and Branding
st.title("🚀 Horizon Automation Engine")
st.caption("Solo Hackathon Prototype | Autonomous Research & Intelligence State Machine")
st.divider()

# Top Row Layout: User Input Settings
col1, col2 = st.columns([3, 1])

with col1:
    user_prompt = st.text_input(
        "Enter target market research query or entity to scan:",
        placeholder="e.g., Stripe API transaction pricing table"
    )

with col2:
    execution_mode = st.selectbox("Execution Mode", ["Live Dynamic Run", "Dry Run Simulation"])

# 🔄 THE INTERACTIVE RUNTIME ENGINE
if st.button("Execute Horizon Graph Engine", type="primary"):
    if not user_prompt.strip():
        st.warning("Please input a valid search query before triggering execution.")
    else:
        st.subheader("⚡ Live Node Execution Logs")
        log_placeholder = st.empty()
        
        # Initialize fresh state array
        state = initial_state.copy()
        state["user_query"] = user_prompt
        state["next_destination"] = "guardrail"
        
        # Visual execution loop mimicking graph routing paths
        with st.spinner("Processing graph tokens..."):
            while True:
                current_target = state["next_destination"]
                
                # --- NODE 1: GUARDRAIL GATE ---
                if current_target == "guardrail":
                    st.info("🔄 `[NODE 1]` Intercepting payload at Security Guardrail Check...")
                    time.sleep(0.5)
                    state = security_guardrail_node(state)
                    
                    if state["is_malicious"]:
                        st.error("❌ `[SECURITY ALERT]` Malicious input signature detected! Halting execution graph.")
                        state["next_destination"] = "end"
                    else:
                        st.success("✅ `[SECURITY PASS]` System Integrity Clear. Query passed safety checks.")
                        state["next_destination"] = "scraper"
                        
                # --- NODE 2: BRIGHT DATA GATE ---
                elif current_target == "scraper":
                    st.info(f"🔄 `[NODE 2]` Routing traffic to Bright Data Residential Proxy Network (Try #{state['retry_count'] + 1})...")
                    state = brightdata_serp_node(state)
                    
                    if not state["scraped_payload"]:
                        if state["retry_count"] < 3:
                            st.warning("⚠️ Payload compilation returned empty. Self-correction loop triggered.")
                            state["next_destination"] = "scraper"
                        else:
                            st.error("❌ Max connection retries exhausted. Terminating loop sequence.")
                            state["next_destination"] = "end"
                    else:
                        st.success("✅ `[DATA RETRIEVED]` Successfully captured live matrix telemetry.")
                        state["next_destination"] = "analytics"
                        
                # --- NODE 3: GEMINI COGNITIVE GATE ---
                elif current_target == "analytics":
                    st.info("🔄 `[NODE 3]` Passing unparsed telemetry cache to Google Gemini 2.5 Flash...")
                    state = analytics_node(state)
                    st.success("✅ `[ANALYSIS COMPLETE]` Intelligence compilation generated.")
                    state["next_destination"] = "end"
                    
                # --- TERMINAL GATEWAY ---
                elif current_target == "end":
                    break
        
        st.divider()
        
        # PRESENTATION LAYER RESULTS Display
        if state["is_malicious"]:
            st.error("### 🛑 Graph Aborted\nThe execution pipeline was killed automatically to protect network infrastructure variables.")
        elif not state["scraped_payload"]:
            st.error("### 💔 Graph Structural Error\nFailed to extract clean web payloads across available retries.")
        else:
            st.success("### 🎉 Graph Execution Complete!")
            
            # Create interactive side-by-side display tabs for telemetry data
            tab1, tab2, tab3 = st.tabs(["🤖 Gemini Agent Insights", "📋 Technical Telemetry", "💾 Raw Cached Payload"])
            
            with tab1:
                st.markdown("### Executive Summary")
                st.write(state["calculated_metrics"].get("agent_insight", "No insights returned."))
                
            with tab2:
                st.markdown("### Graph Metrics")
                st.json({
                    "Timestamp": state["calculated_metrics"].get("execution_timestamp"),
                    "Scraped Characters Logged": state["calculated_metrics"].get("payload_character_count"),
                    "Status Code Mapping": state["calculated_metrics"].get("status"),
                    "Target Routing Zone": "horizon_hackathon_serp_api1",
                    "Total Network Attemps": state["retry_count"]
                })
                
            with tab3:
                st.markdown("### Raw Buffer Cache")
                st.code(state["scraped_payload"])