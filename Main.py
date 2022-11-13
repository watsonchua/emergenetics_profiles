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
                ).sort_values('NAME', ascending=True)
            # './profile.csv')

def main():
    read_data()

    df_profiles = st.session_state['df_profile']

    st.set_page_config(
        layout="wide",
        page_title="AIPF Emergenetics Profiles"
        )
    st.title("AIPF Emergenetics Profiles")

    labels = ['ANALYTICAL', 'CONCEPTUAL','STRUCTURAL', 'SOCIAL']

    with st.container():
        mean_values = df_profiles[labels].mean().to_numpy()

        fig, ax = plt.subplots()
        ax.pie(mean_values, labels=labels, autopct='%1.2f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        st.write('AIPF Overall')
        st.pyplot(fig)
        plt.close(fig)

    for l in labels:
        with st.expander('Top 5: ' + l.title()):
            df_top = df_profiles.nlargest(5, l).sort_values(l, ascending=True)
            fig=px.bar(df_top, y='NAME', x=l, orientation='h',color=l)
            st.write(fig)


    
   


if __name__ == "__main__":
    main()
