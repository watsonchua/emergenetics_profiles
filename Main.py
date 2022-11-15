import streamlit as st
import pandas as pd
from datetime import datetime
from time import perf_counter
import toml
import matplotlib.pyplot as plt
import math
import plotly.express as px
import numpy as np
import boto3

# @st.cache(ttl=1*60*60)
def read_data():
    secrets = toml.load('.streamlit/secrets.toml')
    aws_access_key_id = secrets['aws_access_key_id']
    aws_secret_access_key = secrets['aws_secret_access_key']

    s3_client = boto3.client('s3', 
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    if 'df_profile' not in st.session_state:
        st.session_state['df_profile'] = pd.read_csv(
            f"s3://aipf-emergenetics/profile.csv",
                storage_options={
                    "key": aws_access_key_id,
                    "secret": aws_secret_access_key
                }
                ).sort_values('Name', ascending=True)


    # if 'cosine_similarity_matrix' not in st.session_state:
    #     s3_client.download_file('aipf-emergenetics', 'cosine_similarity.npy')
    #     st.session_state['cosine_similarity'] = np.load('cosine_similarity.npy')



def main():
    read_data()

    df_profiles = st.session_state['df_profile']

    st.set_page_config(
        layout="wide",
        page_title="AIPF Emergenetics Profiles"
        )
    st.title("AIPF Emergenetics Profiles")

    attributes = ['Analytical', 'Conceptual','Structural', 'Social']
    attribute_percentile = ['Analytical Percentile', 'Conceptual Percentile','Structural Percentile', 'Social Percentile']
    behaviour_percentile = ['Expressiveness', 'Assertiveness','Flexibility']


    with st.container():
        mean_attribute_values = df_profiles[attributes].mean().to_numpy()
        df_mean_behaviour = df_profiles[behaviour_percentile].mean().round(2)


        fig, ax = plt.subplots()
        ax.pie(mean_attribute_values, labels=attributes, autopct='%1.2f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        st.header('AIPF Average')
        column_1, column_2 = st.columns(2)
        column_1.pyplot(fig)
        plt.close(fig)


        fig_behavioural =px.bar(df_mean_behaviour.transpose().to_frame(name='Mean Percentile'), x='Mean Percentile', orientation='h', color='Mean Percentile', range_x=[0,100])
        st.write(fig_behavioural)




    with st.container():
        st.header('Attribute Leaderboard')
        for l in attribute_percentile:
            write_top_and_bottom(df_profiles, l)
            

    with st.container():
        st.header('Behavioural Leaderboard')
        for l in behaviour_percentile:
            write_top_and_bottom(df_profiles, l)
            
def write_top_and_bottom(df_prof, label, top_k=10):
    df_top = df_prof.nlargest(top_k, label).sort_values(label, ascending=True)
    df_bottom = df_prof.nsmallest(top_k, label).sort_values(label, ascending=True)
    fig_top = px.bar(df_top, y='Name', x=label, orientation='h',color=label, range_x=[0,100])
    fig_bottom = px.bar(df_bottom, y='Name', x=label, orientation='h',color=label, range_x=[0,100])

    with st.expander(label.title().replace('Percentile', '')):
        st.markdown('#### Top 10')
        st.write(fig_top)
        st.markdown('#### Bottom 10')
        st.write(fig_bottom)

if __name__ == "__main__":
    main()
