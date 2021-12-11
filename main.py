######################
# Import libraries
######################

import pandas as pd
import streamlit as st

import os



def score(transactions_csv_file_path,n):

	filenames = os.listdir(transactions_csv_file_path)
	selected_filename = st.selectbox("Select A file",filenames)
	return [os.path.join(transactions_csv_file_path,selected_filename),n]

number = st.number_input('Enter n, max=100',1, 100)

scores = score(transactions_csv_file_path='./test_data',n=number) 

n=scores[1]
st.write(scores)
st.info("You Selected {}".format(scores[0]))
df = pd.read_csv(scores[0])
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
st.text("The first five records")
st.dataframe(df.head())


x = df.sort_values(by=['customer_id', 'transaction_date']).drop_duplicates(["transaction_date", "customer_id"])
st.text("Sorted records by date and customer id")
st.dataframe(x)
m = (x.assign(transaction_date=pd.to_datetime(x['transaction_date']))
       .groupby('customer_id')['transaction_date']
       .diff()
       .gt(pd.Timedelta('1D'))
       .cumsum())
df1 = x.groupby(['customer_id', m]).size().max(level='customer_id').sort_values(ascending=False)

# number = st.number_input('Insert a number',1, 10)
# st.write('The current number is ', number)
st.text("Sorted records based on 'n value input'")
st.dataframe(df1.head(n))
st.text("Final output")
st.info(df1.head(n).index.get_level_values(0))



          
