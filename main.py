######################
# Import libraries
######################

import pandas as pd
import streamlit as st
import altair as alt

import os
import seaborn as sns


def score(transactions_csv_file_path,n):

	filenames = os.listdir(transactions_csv_file_path)
	selected_filename = st.selectbox("Select A file",filenames)
	return os.path.join(transactions_csv_file_path,selected_filename)


scores = score(transactions_csv_file_path='./test_data',n=0) 
st.write(scores)
st.info("You Selected {}".format(scores))
df = pd.read_csv(scores)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
# if st.checkbox("Show Dataset"):
# number = st.double_input("Number of Rows to View")
st.dataframe(df.head())
st.dataframe(df[df['customer_id']=='K20008'])


x = df.sort_values('transaction_date', ascending=0)


x["subgroup"] = x["customer_id"].ne(x["customer_id"].shift()).cumsum()

# take the max length of any subgroup that belongs to "name"
def get_max_consecutive(customers):
    return x.groupby(["customer_id", "subgroup"]).apply(len)[customers].max()
l=[]
for customers in x.customer_id.unique():
    
    l.append(f"{customers}: {get_max_consecutive(customers)}")   
st.info(l)           
