#!/bin/sh
python3 pdf_to_df.py
aws s3 cp profile.csv s3://aipf-emergenetics/
aws s3 cp cosine_similarity.npy s3://aipf-emergenetics/
