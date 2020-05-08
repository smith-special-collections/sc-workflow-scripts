import pandas as pd

gformb = pd.read_csv("(responses) COVID-19 Chronicles electronic file upload form - Form Responses 1.csv")
gforma = pd.read_csv("Covid-19 Chronicles contributor form (Responses) - Form Responses 1-2.csv")

merged = pd.merge(gformb, gforma, how='left', on=['Email Address'])
merged.to_csv("merged_responses.csv", index=False)

new_headers=['nanci_checkB1','copyright','nanci_checkB2','agent_id','timestampB','email','file1','file1_date','file1_upload','anotherfile1','file2','file2_date','file2_upload','anotherfile2','file3','file3_date','file3_upload','anotherfile3','file4','file4_date','file4_upload','anotherfile4','file5','file5_date','file5_upload','anotherfile5','file6','file6_date','file6_upload','anotherfile6','file7','file7_date','file7_upload','anotherfile7','file8','file8_date','file8_upload','anotherfile8','file9','file9_date','file9_upload','anotherfile9','file10','file10_date','file10_upload','readytosubmit','comments','nanci_checkA','timestampA','first_name','last_name','full_name','legal_name','affiliation','where_living','bioghist','created','med_info','access','digital_files_yn','online_content_yn','content_description','number_of_files','file_types','physical_material_yn','phys_content_description','questions']
renamed = pd.read_csv("merged_responses.csv",skiprows=1,names=new_headers,low_memory=False)
renamed.to_csv("merged_responses_newheaders.csv", index=False)