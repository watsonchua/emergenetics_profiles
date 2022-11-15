from glob import glob
import re
from tika import parser
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


percentile_patterns = r"The Percentiles\n\nAnalytical (\d+)%ile\n\nStructural (\d+)%ile\n\nSocial (\d+)%ile\n\nConceptual (\d+)%ile\n\nBar charts in four colors show your Thinking Attributes in percentiles."


conceptual_pattern = r"CONCEPTUAL = (\d+)%"
analytical_pattern = r"ANALYTICAL = (\d+)%"
structural_pattern = r"STRUCTURAL = (\d+)%"
social_pattern = r"SOCIAL = (\d+)%"

other_patterns = r"Expressiveness (\d+)%ile\n\nAssertiveness (\d+)%ile\n\nFlexibility (\d+)%ile"
name_pattern = r"Congratulations,(.*)!"

def extract_values(text):
    name = re.findall(name_pattern, text)[0]
    analytical_percentile, structural_percentile, social_percentile, conceptual_percentile = re.findall(percentile_patterns, text)[0]
    analytical_percentage = re.findall(analytical_pattern, text)[0]
    structural_percentage = re.findall(structural_pattern, text)[0]
    social_percentage = re.findall(social_pattern, text)[0]
    conceptual_percentage = re.findall(conceptual_pattern, text)[0]
    expressiveness, assertiveness, flexibility = re.findall(other_patterns, text)[0]

    return {
        'Name': name.title().strip(),
        'Analytical': analytical_percentage, 
        'Conceptual': conceptual_percentage,
        'Structural': structural_percentage, 
        'Social': social_percentage, 
        'Analytical Percentile': analytical_percentile,
        'Conceptual Percentile': conceptual_percentile, 
        'Structural Percentile': structural_percentile, 
        'Social Percentile': social_percentile, 
        'Expressiveness': expressiveness, 
        'Assertiveness': assertiveness, 
        'Flexibility': flexibility
    }


def main():
    filepaths = glob('./AIPF Emergenetics Profile/*.pdf')
    profiles = []
    for fp in filepaths:
        print(fp)
        parsed_pdf = parser.from_file(fp)
        content = parsed_pdf['content']    
        if not content.strip().endswith('Please contact your Emergenetics Associate or email the Emergenetics International\noffice at brains@emergenetics.com with your observations, suggestions, and comments.\n\n \n\nNOTES'):
            print('Invalid file')
            continue
        extracted = extract_values(content)
        profiles.append(extracted)


    # create profiles dataframe
    df_profiles = pd.DataFrame(profiles)
    df_profiles.to_csv('profile.csv', index=False)

    # create similarity matrix
    cos_sim = cosine_similarity(df_profiles[['Analytical', 'Conceptual', 'Structural', 'Social']])
    np.save('cosine_similarity.npy', cos_sim)


