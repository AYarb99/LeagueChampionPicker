import streamlit as st
import pandas as pd

# --- Data ---
data = {
    'Champion': ['Jinx', 'Ashe', 'Tristana', 'Caitlyn', 'Ziggs', 'Vayne', 'Varus', 'Sivir', 'Kaisa', 'Miss Fortune'],
    'Blind Pick': [6.83, 8.54, 5.12, 5.98, 7.68, 0.85, 5.98, 4.27, 3.41, 5.98],
    'Tank Shred': [5.79, 4.97, 4.97, 4.14, 6.62, 8.28, 6.62, 3.31, 5.79, 4.14],
    'Burst Damage': [3.15, 2.10, 6.30, 7.35, 5.25, 3.15, 8.41, 2.10, 6.30, 10.51],
    'Self Peel': [4.79, 6.71, 6.71, 4.79, 5.75, 8.63, 1.92, 5.75, 8.63, 0.96],
    'Teamfight': [8.41, 3.36, 5.04, 5.04, 7.57, 3.36, 4.20, 5.88, 3.36, 8.41],
    'Skirmish': [3.21, 7.23, 7.23, 4.02, 6.43, 7.23, 5.62, 2.41, 8.03, 3.21],
    'Carry Potential': [8.33, 3.70, 7.41, 5.56, 6.48, 3.70, 5.56, 2.78, 4.63, 6.48],
    'Utility': [5.91, 14.77, 2.95, 4.43, 11.81, 2.95, 4.43, 1.48, 1.48, 4.43],
    'Wave Clear': [7.54, 5.65, 5.65, 3.77, 6.59, 0.94, 6.59, 9.42, 3.77, 4.71],
    'AP': [0.00, 0.00, 0.00, 0.00, 23.75, 0.00, 11.88, 0.00, 19.00, 0.00],
    'Lane Dominance': [3.15, 7.35, 8.41, 7.35, 3.15, 1.05, 5.25, 8.41, 4.20, 6.30]
}

league_df = pd.DataFrame(data)
columns = [c for c in league_df.columns if c != 'Champion']

st.set_page_config(page_title="League Champion Picker", layout="wide")
st.title("🏆 League Champion Picker")

# --- Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Select Key Attributes")
    st.caption("Pick which stats matter most to you.")
    selected = []
    cols = st.columns(3)
    for i, c in enumerate(columns):
        with cols[i % 3]:
            if st.checkbox(c, key=f"chk_{c}"):
                selected.append(c)

with col2:
    st.subheader("Adjust Weights")
    st.caption("Only active for selected stats.")
    weights = {}
    cols = st.columns(2)
    for i, c in enumerate(selected):
        with cols[i % 2]:
            weights[c] = st.slider(c, 0.0, 5.0, 1.0, 0.1, key=f"w_{c}")

# Fill unselected with zero
for c in columns:
    if c not in weights:
        weights[c] = 0.0

# --- Scoring ---
weight_series = pd.Series(weights)
league_df['Score'] = league_df[columns].dot(weight_series)
ranked = league_df.sort_values(by='Score', ascending=False).reset_index(drop=True)

# --- Results ---
st.markdown("### 🧮 Champion Rankings")
st.dataframe(ranked[['Champion', 'Score']], use_container_width=True, height=300)

if st.button("🔄 Reset"):
    st.cache_data.clear()
    st.experimental_rerun()

st.caption("Choose your preferred attributes, assign importance, and see who comes out on top!")