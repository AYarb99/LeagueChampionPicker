import streamlit as st
import pandas as pd
import numpy as np

# --- Step 1: Raw integer scores (approximate original table 0-10) ---
raw_data = {
    'Champion': ['Jinx', 'Ashe', 'Tristana', 'Caitlyn', 'Ziggs', 'Vayne', 'Varus', 'Sivir', 'Kaisa', 'Miss Fortune'],
    'Blind Pick': [7, 9, 5, 6, 8, 1, 6, 4, 3, 6],
    'Tank Shred': [6, 5, 5, 4, 7, 10, 8, 3, 7, 4],
    'Burst Damage': [3, 2, 7, 8, 6, 3, 8, 2, 7, 10],
    'Self Peel': [3, 7, 7, 5, 6, 9, 2, 6, 9, 1],
    'Teamfight': [10, 6, 5, 6, 8, 3, 7, 6, 3, 9],
    'Skirmish': [4, 7, 8, 4, 6, 9, 6, 2, 10, 3],
    'Carry Potential': [9, 5, 7, 6, 6, 4, 5, 3, 5, 6],
    'Utility': [3, 10, 4, 5, 8, 3, 7, 3, 1, 5],
    'Wave Clear': [8, 4, 6, 5, 7, 1, 7, 9, 4, 4],
    'AP': [0, 0, 0, 0, 10, 0, 5, 0, 8, 0],
    'Lane Dominance': [3, 7, 9, 7, 3, 1, 5, 9, 4, 8]
}


league_df = pd.DataFrame(raw_data)
columns = [c for c in league_df.columns if c != 'Champion']

# --- Step 2: Reweighting function ---
def reweight(df, cols):
    weighted_df = df.copy()
    expected_avg = df[cols].sum().sum() / len(cols) / len(df)  # target average across all cols
    for col in cols:
        actual_avg = df[col].mean()
        weighted_df[col] = df[col] * (expected_avg / actual_avg)
    return weighted_df

weighted_df = reweight(league_df, columns)

# --- Streamlit dashboard ---
st.set_page_config(page_title="League Champion Picker", layout="wide")
st.title("🏆 League Champion Picker")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Select Key Attributes")
    st.caption("Pick which stats matter most to you.")
    selected = []
    cols_ui = st.columns(3)
    for i, c in enumerate(columns):
        with cols_ui[i % 3]:
            if st.checkbox(c, key=f"chk_{c}", value=True):
                selected.append(c)

with col2:
    st.subheader("Adjust Weights")
    st.caption("Only active for selected stats.")
    weights = {}
    cols_ui = st.columns(2)
    for i, c in enumerate(selected):
        with cols_ui[i % 2]:
            weights[c] = st.slider(c, 0.0, 5.0, 1.0, 0.1, key=f"w_{c}")

# Fill unselected with zero
for c in columns:
    if c not in weights:
        weights[c] = 0.0

# --- Compute final scores ---
weight_series = pd.Series(weights)
weighted_df['Score'] = weighted_df[columns].dot(weight_series)
ranked = weighted_df.sort_values(by='Score', ascending=False).reset_index(drop=True)

# --- Display ---
st.markdown("### 🧮 Champion Rankings")
st.dataframe(ranked[['Champion', 'Score']], use_container_width=True, height=300)

if st.button("🔄 Reset"):
    st.cache_data.clear()
    st.experimental_rerun()

st.caption("Choose your preferred attributes, assign importance, and see who comes out on top!")
