import streamlit as st
from langchain_core.messages import HumanMessage
from main import app as graph_app

# Set Page Configuration
st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for styling cards, images, and labels
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; text-align: center; margin-bottom: 0px; }
    .sub-title { font-size: 1rem; color: #888; text-align: center; margin-bottom: 25px; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: 600; }
    .metric-card {
        background-color: #1e2530;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #2d3748;
    }
    .metric-num { font-size: 1.8rem; font-weight: bold; color: #3182ce; }
    .metric-label { font-size: 0.85rem; color: #a0aec0; }
    </style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR CONFIG -----------------
st.sidebar.title("✈️ AI Travel Planner")

# Dynamic Thread ID / User ID Input
user_id = st.sidebar.text_input(
    "👤 User ID", 
    value="Arooj_User",
    help="Changing this ID resets the state memory in PostgreSQL for a clean run."
)

st.sidebar.markdown("---")
st.sidebar.caption("Powered by")
st.sidebar.info("""
- **LangGraph**
- **Groq** (`openai/gpt-oss-120b`)
- **PostgreSQL Checkpointer**
- **Tavily & AviationStack Tools**
""")

st.sidebar.markdown("---")
st.sidebar.subheader("Agent Pipeline")
st.sidebar.markdown("""
1. ✈️ **Flight Agent**
2. 🏨 **Hotel Agent**
3. 🗺️ **Itinerary Agent**
4. 🏁 **Final Agent**
""")

# ----------------- MAIN TITLE -----------------
st.markdown("<div class='main-title'>✈️ AI Travel Booking System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Four specialized agents work together — searching flights, hotels, building an itinerary, and delivering your perfect trip plan.</div>", unsafe_allow_html=True)

# ----------------- DESTINATION IMAGES SECTION -----------------
DESTINATIONS = [
    ("JP Tokyo", "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=500"),
    ("FR Paris", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=500"),
    ("TH Bangkok", "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=500"),
    ("IT Rome", "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=500"),
    ("AE Dubai", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=500")
]

cols = st.columns(5)
for col, (name, img_url) in zip(cols, DESTINATIONS):
    with col:
        # Destination image cards container
        st.markdown(f"""
            <div style="border-radius:10px; overflow:hidden; position:relative; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <img src="{img_url}" style="width:100%; height:110px; object-fit:cover; display:block;">
                <div style="position:absolute; bottom:8px; left:8px; color:#fff; font-size:0.85rem; font-weight:bold; background:rgba(0,0,0,0.6); padding:2px 8px; border-radius:4px;">
                    📍 {name}
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- QUICK PRESETS -----------------
col1, col2, col3, col4 = st.columns(4)
preset_query = None

with col1:
    if st.button("7-day Japan under ₹2L"):
        preset_query = "Plan a complete 7 days Japan trip including flights, hotels and sightseeing under 200000 PKR."
with col2:
    if st.button("Paris trip for 5 days"):
        preset_query = "Plan a complete 5 days Paris trip with budget hotels and flights in PKR."
with col3:
    if st.button("Dubai weekend trip"):
        preset_query = "Plan a 3-day weekend trip to Dubai under 150000 PKR."
with col4:
    if st.button("Bali backpacking 10 days"):
        preset_query = "Plan a complete 7 days plan of Bali trip including flights, hotels, and sightseeing under 150000 PKR."

st.markdown("### 📝 DESCRIBE YOUR TRIP")
initial_val = preset_query if preset_query else ""
user_prompt = st.text_area("Trip Request:", value=initial_val, height=90, placeholder="Plan a complete 7 days plan of Bali trip including flights, hotels, and sightseeing under 150000 PKR")

generate_btn = st.button("🚀 Generate My Travel Plan", type="primary")

# ----------------- AGENT EXECUTION & METRICS DISPLAY -----------------
if generate_btn and user_prompt.strip():
    config = {
        "configurable": {
            "thread_id": user_id.strip()
        }
    }
    
    with st.spinner("Agents working in pipeline..."):
        try:
            input_state = {
                "message": [HumanMessage(content=user_prompt)],
                "user_query": user_prompt
            }
            
            # Execute graph
            output = graph_app.invoke(input_state, config=config)
            
            # --- STATUS METRICS STRIP ---
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-num">4</div>
                        <div class="metric-label">AGENTS RUN</div>
                    </div>
                """, unsafe_allow_html=True)
            with m_col2:
                llm_calls_count = output.get("llm_calls", 4)
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-num">{llm_calls_count}</div>
                        <div class="metric-label">LLM CALLS</div>
                    </div>
                """, unsafe_allow_html=True)
            with m_col3:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-num" style="color: #48bb78;">🟢</div>
                        <div class="metric-label">STATUS COMPLETE</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- AGENT INDIVIDUAL OUTPUT TABS ---
            st.subheader("🔍 Agent Intermediate Outputs")
            tab_flight, tab_hotel, tab_itinerary = st.tabs(["✈️ Flight Agent Result", "🏨 Hotel Agent Result", "🗺️ Itinerary Agent Result"])
            
            with tab_flight:
                st.info(output.get("flight_results", "No flight data recorded."))
            with tab_hotel:
                st.info(output.get("hotel_results", "No hotel data recorded."))
            with tab_itinerary:
                st.info(output.get("itinerary", "No raw itinerary data recorded."))

            st.markdown("---")
            
            # --- FINAL TRAVEL PLAN DISPLAY ---
            st.subheader("🌸 Final Travel Plan")
            final_plan_text = ""
            
            if "itinerary" in output and output["itinerary"]:
                final_plan_text = output["itinerary"]
            elif "message" in output and len(output["message"]) > 0:
                final_plan_text = output["message"][-1].content
            else:
                final_plan_text = str(output)
                
            st.markdown(final_plan_text)
            
            # --- DOWNLOAD BUTTON ---
            st.download_button(
                label="📥 Download Complete Travel Plan (.txt)",
                data=final_plan_text,
                file_name=f"travel_plan_{user_id}.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"Error executing agent workflow: {str(e)}")