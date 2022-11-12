import streamlit as st
import pandas as pd
from datetime import datetime
from time import perf_counter
import toml
import matplotlib.pyplot as plt
import math


# secrets = toml.load('.streamlit/secrets.toml')
# es_username = secrets['es_username']
# es_password = secrets['es_password']


@st.cache(ttl=1*60*60)
def read_data():
    df = pd.read_csv('./profile.csv')
    return df.sort_values('NAME', ascending=True)

def make_grid(num_rows,num_cols):
    grid = [0]*num_rows
    for i in range(num_rows):
        with st.container():
            grid[i] = st.columns(num_cols)
    return grid

def main():
    st.set_page_config(
        layout="wide",
        page_title="AIPF Emergenetics Profiles"
        )
    st.title("AIPF Emergenetics Profiles")

    labels = ['ANALYTICAL', 'CONCEPTUAL','STRUCTURAL', 'SOCIAL']
    
    df_profiles = read_data()
    num_cols = 3
    num_rows = math.ceil(len(df_profiles)/num_cols)

    st.sidebar.title("Filters")

    names_container = st.sidebar.container()

    all_names = ['All'] + df_profiles['NAME'].to_list()
    names_filter = names_container.multiselect('Name(s)', all_names, default=all_names)
    if 'All' in names_filter:
        names_filter = all_names


    with st.container():
        df_filtered = df_profiles[df_profiles['NAME'].isin(names_filter)]
        grid = make_grid(num_rows, num_cols)
        row_no = 0
        col_no = 0
        counter = 0       
        for index, row in df_filtered.iterrows():
            row_values = row[labels].values
            fig, ax = plt.subplots()
            ax.pie(row_values, labels=labels, autopct='%1.0f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            cell = grid[row_no][col_no]
            cell.write(row['NAME'])
            cell.pyplot(fig)
            plt.close(fig)

            counter += 1
            row_no = counter // num_cols
            col_no = counter % num_cols


if __name__ == "__main__":
    main()
