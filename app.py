import streamlit as st
import pandas as pd
from io import StringIO, BytesIO

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

def convert_to_lms_format(df):
    lms_output = []
    for _, row in df.iterrows():
        question = row['Question']
        correct_answer = row[f"Answer {row['Correct']}"]
        incorrect_answers = [row[f'Answer {i}'] for i in range(1, 5) if i != row['Correct']]
        
        lms_format = f"Typ\tSC\nLevel\tWissen\nTitle\t{question[:50]}...\nQuestion\t{question}\nPoints\t1\n1\t{correct_answer}\n" + \
                     "\n".join([f"-0.5\t{answer}" for answer in incorrect_answers])
        lms_output.append(lms_format)
    
    return "\n\n".join(lms_output)

st.title("Table to Excel and LMS Format Converter for Kahoot")
st.write("Paste your CSV data in the text area below. Use slash (/) to separate columns and new lines to separate rows.")

csv_input = st.text_area("Input your CSV data here:", height=300)

if st.button("Convert and Download"):
    try:
        df = pd.read_csv(StringIO(csv_input), sep=' / ', engine='python')
        df.columns = ["Question", "Answer 1", "Answer 2", "Answer 3", "Answer 4", "Time", "Correct"]
        
        st.write("Here is a preview of your data:")
        st.write(df)
        
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name="table.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        lms_data = convert_to_lms_format(df)
        st.download_button(
            label="Download LMS Format",
            data=lms_data,
            file_name="lms_import.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
