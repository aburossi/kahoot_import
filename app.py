import streamlit as st
import pandas as pd
from io import StringIO, BytesIO

# Function to convert DataFrame to Excel
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# Streamlit UI
st.title("Table to Excel Converter")

st.write("Paste your CSV data in the text area below. Use comma to separate columns and new lines to separate rows.")
csv_input = st.text_area("Input your CSV data here:", height=300)

if st.button("Convert and Download Excel"):
    try:
        df = pd.read_csv(StringIO(csv_input))
        st.write("Here is a preview of your data:")
        st.write(df)
        
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name="table.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
