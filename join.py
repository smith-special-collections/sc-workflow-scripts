import pandas as pd

gformb = pd.read_csv("(responses) COVID-19 Chronicles electronic file upload form - Form Responses 1.csv")
gforma = pd.read_csv("Covid-19 Chronicles contributor form (Responses) - Form Responses 1-2.csv")

merged = pd.merge(gformb, gforma, how='left', on=['Email Address'])
merged.to_csv("merged_respones.csv", index=False)
