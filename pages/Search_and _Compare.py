import streamlit as st
import pandas as pd
from datetime import datetime
from time import perf_counter
import toml
import matplotlib.pyplot as plt
import math
from Main import read_data
from sklearn.metrics.pairwise import cosine_similarity


# secrets = toml.load('.streamlit/secrets.toml')
# es_username = secrets['es_username']
# es_password = secrets['es_password']


# @st.cache(ttl=1*60*60)
# def read_data():
#     if 'df_profile' not in st.session_state:
#         st.session_state['df_profile'] = pd.read_csv('./profile.csv').sort_values('NAME', ascending=True)
#     if 'df_names' not in st.session_state:
#         st.session_state['df_names'] = pd.read_csv('./aipf_names.csv').sort_values('Name', ascending=True)
#     # return df.sort_values('NAME', ascending=True)

def make_grid(num_rows,num_cols):
    grid = [0]*num_rows
    for i in range(num_rows):
        with st.container():
            grid[i] = st.columns(num_cols)
    return grid

def main():
    read_data()

    df_profiles = st.session_state['df_profile']

    st.set_page_config(
        layout="wide",
        page_title="AIPF Emergenetics Profiles"
        )
    st.title("AIPF Emergenetics Profiles")

    labels = ['ANALYTICAL', 'CONCEPTUAL','STRUCTURAL', 'SOCIAL']
    

    st.sidebar.title("Filters")
    
    names_container = st.sidebar.container()

    names_container.info('Select one profile to see profiles most similar to it.   \n  \nSelect two profiles to see their similarity score.  \n  \nSelect three or more profiles for visual comparison.')

    all_names = ['All'] + df_profiles['NAME'].to_list()
    names_filter = names_container.multiselect('Name(s)', all_names, default=all_names)
    if 'All' in names_filter:
        names_filter = all_names


    with st.container():
        df_filtered = df_profiles[df_profiles['NAME'].isin(names_filter)]
        if len(df_filtered) < 3:
            num_rows = 1
            num_cols = max(1, len(df_filtered))
        else:
            num_cols = 3
            num_rows = math.ceil(len(df_filtered)/num_cols)

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
        
        if len(df_filtered) == 2:
            compare_vectors = df_filtered[labels].to_numpy()
            similarity_score = cosine_similarity(compare_vectors[0].reshape(1,-1), compare_vectors[1].reshape(1,-1))
            with st.container():
                st.write('Similarity: ' + "{:.3f}".format(similarity_score[0][0]))

        


if __name__ == "__main__":
    main()
