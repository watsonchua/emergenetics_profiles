import streamlit as st
import pandas as pd
from datetime import datetime
from time import perf_counter
import toml
import matplotlib.pyplot as plt
import math
import plotly.express as px



# secrets = toml.load('.streamlit/secrets.toml')
# es_username = secrets['es_username']
# es_password = secrets['es_password']


# @st.cache(ttl=1*60*60)
def read_data():
    if 'df_profile' not in st.session_state:
        st.session_state['df_profile'] = pd.read_csv('./profile.csv').sort_values('NAME', ascending=True)
    # if 'df_names' not in st.session_state:
        # st.session_state['df_names'] = pd.read_csv('./aipf_names.csv').sort_values('Name', ascending=True)
    # return df.sort_values('NAME', ascending=True)

# def make_grid(num_rows,num_cols):
#     grid = [0]*num_rows
#     for i in range(num_rows):
#         with st.container():
#             grid[i] = st.columns(num_cols)
#     return grid

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
