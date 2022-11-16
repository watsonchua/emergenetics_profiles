import streamlit as st
import pandas as pd
from datetime import datetime
from time import perf_counter
import toml
import matplotlib.pyplot as plt
import math
from Main import read_data
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px


def make_grid(num_rows,num_cols):
    grid = [0]*num_rows
    for i in range(num_rows):
        with st.container():
            grid[i] = st.columns(num_cols)
    return grid

def main():
    read_data()

    df_profiles = st.session_state['df_profile']
    df_cosine_similarity = st.session_state['df_cosine_similarity']

    st.set_page_config(
        layout="wide",
        page_title="AIPF Emergenetics Profiles"
        )
    st.title("AIPF Emergenetics Profiles")

    attributes = ['Analytical', 'Conceptual','Structural', 'Social']
    behavioural = ['Expressiveness', 'Assertiveness','Flexibility']
    

    st.sidebar.title("Filters")
    
    names_container = st.sidebar.container()

    names_container.info('Select one profile to see profiles most similar/dissimilar to it.   \n  \nSelect two profiles to see their similarity score.  \n  \nSelect three or more profiles for visual comparison.')

    all_names = ['All'] + df_profiles['Name'].to_list()
    names_filter = names_container.multiselect('Name(s)', all_names, default=all_names)
    if 'All' in names_filter:
        names_filter = all_names


    with st.container():
        df_filtered = df_profiles[df_profiles['Name'].isin(names_filter)]
        if len(df_filtered) < 3:
            num_rows = 1
            num_cols = 2
        else:
            num_cols = 3
            num_rows = math.ceil(len(df_filtered)/num_cols)

        grid = make_grid(num_rows, num_cols)
        row_no = 0
        col_no = 0
        counter = 0       
        for index, row in df_filtered.iterrows():
            attribute_values = row[attributes].values
            fig, ax = plt.subplots()
            ax.pie(attribute_values, labels=attributes, autopct='%1.0f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            cell = grid[row_no][col_no]
            if row['Name'] == 'Watson Chua':
                cell.markdown('<b>' + row['Name'] + '</b>' + ' <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Twitter_Verified_Badge.svg/512px-Twitter_Verified_Badge.svg.png" width="20"/>', unsafe_allow_html=True)
            else:
                cell.markdown('<b>' + row['Name'] + '</b>', unsafe_allow_html=True)
                # cell.write('**'+row['Name'] + '**')
            cell.write('"'+ row['Motto'] + '"')
            cell.pyplot(fig)
            plt.close(fig)


            # behavourial_values = row[behavioural].values
            # cell.bar_chart(behavourial_values, x=behavioural)
            # fig1, ax1 = plt.subplots()
            # fig1 = px.bar(data_frame=row[behavioural], orientation='h')
            # cell.pyplot(fig1)
            # plt.close(fig1)



            counter += 1
            row_no = counter // num_cols
            col_no = counter % num_cols
        
        if len(df_filtered) == 2:
            # compare_vectors = df_filtered[attributes].to_numpy()
            # similarity_score = cosine_similarity(compare_vectors[0].reshape(1,-1), compare_vectors[1].reshape(1,-1))
            with st.container():
                _, column_2, _ = st.columns(3)
                name_1 = df_filtered.iloc[0]['Name']
                name_2 = df_filtered.iloc[1]['Name']
                # print(df_cosine_similarity)
                # print(df_cosine_similarity.columns)
                column_2.header('Similarity: ' + "{:.3f}".format(df_cosine_similarity[name_1][name_2]))

        if len(df_filtered) == 1:
            name = df_filtered.iloc[0]['Name']
            df_most_similar = df_cosine_similarity[name].nlargest(6)[1:]
            df_most_dissimilar = df_cosine_similarity[name].nsmallest(5)

            sim_cell = grid[0][1]
            sim_cell.write('Most Similar')
            sim_cell.table(df_most_similar.to_frame('Score'))

            sim_cell.write('Most Different')
            sim_cell.table(df_most_dissimilar.to_frame('Score').sort_values('Score', ascending=False))

        


if __name__ == "__main__":
    main()
