import streamlit as st
import pandas as pd
from datetime import datetime
from time import perf_counter
import toml
import matplotlib.pyplot as plt
import math
import plotly.express as px

# @st.cache(ttl=1*60*60)
def read_data():
    secrets = toml.load('.streamlit/secrets.toml')
    aws_access_key_id = secrets['aws_access_key_id']
    aws_secret_access_key = secrets['aws_secret_access_key']

    if 'df_profile' not in st.session_state:
        st.session_state['df_profile'] = pd.read_csv(
            f"s3://aipf-emergenetics/profile.csv",
                storage_options={
                    "key": aws_access_key_id,
                    "secret": aws_secret_access_key
                }
                ).sort_values('Name', ascending=True)
            # './profile.csv')

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
        mean_values = df_profiles[attributes].mean().to_numpy()

        fig, ax = plt.subplots()
        ax.pie(mean_values, labels=attributes, autopct='%1.2f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        st.header('AIPF Overall')
        _, column_2, _ = st.columns(3)
        column_2.pyplot(fig)
        plt.close(fig)

    with st.container():
        st.header('Attribute')
        for l in attribute_percentile:
            with st.expander('Top 5: ' + l.title()):
                df_top = df_profiles.nlargest(5, l).sort_values(l, ascending=True)
                fig=px.bar(df_top, y='Name', x=l, orientation='h',color=l)
                st.write(fig)

    with st.container():
        st.header('Behavioural')
        for l in behaviour_percentile:
            with st.expander('Top 5: ' + l.title()):
                df_top = df_profiles.nlargest(5, l).sort_values(l, ascending=True)
                fig=px.bar(df_top, y='Name', x=l, orientation='h',color=l)
                st.write(fig)


    
   


if __name__ == "__main__":
    main()
