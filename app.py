import streamlit as st
import pandas as pd
from io import BytesIO

# Function to convert DataFrame to Excel
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# Streamlit UI
st.title("Table to Excel Converter")

st.write("Upload your CSV file with the table data.")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Here is a preview of your data:")
        st.write(df)
        
        if st.button("Convert and Download Excel"):
            excel_data = convert_df_to_excel(df)
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name="table.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"An error occurred: {e}")
