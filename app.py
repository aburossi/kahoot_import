import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO, BytesIO

def convert_df_to_excel(df):
    # Shuffle answers for each question
    for i in range(len(df)):
        answers = df.iloc[i, 1:5].tolist()
        correct_index = df.iloc[i, 6] - 1
        correct_answer = answers[correct_index]
        
        # Shuffle answers
        np.random.shuffle(answers)
        
        # Update DataFrame with shuffled answers
        df.iloc[i, 1:5] = answers
        
        # Update correct answer index
        df.iloc[i, 6] = answers.index(correct_answer) + 1

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

# New function for H5P format
def convert_to_h5p_format(df):
    h5p_output = []
    for _, row in df.iterrows():
        question = row['Question']
        correct_answer = row[f"Answer {row['Correct']}"]
        incorrect_answers = [row[f'Answer {i}'] for i in range(1, 5) if i != row['Correct']]
        
        # Format: Correct answer first, followed by incorrect answers
        h5p_format = f"{question}\n{correct_answer}\n" + "\n".join(incorrect_answers)
        h5p_output.append(h5p_format)
    
    return "\n\n".join(h5p_output)

st.title("Table to Excel for Kahoot-Import")
st.write("Paste your data in the text area below. Use slash (/) to separate columns and new lines to separate rows. Use this [customGPT](https://chatgpt.com/g/g-hKBP1U4Ks-kahoot-streamlit) first to generate the data")

csv_input = st.text_area("Input your data here:", height=300)

if st.button("Convert and Download"):
    try:
        # Adjusted separator to handle spaces around slash
        df = pd.read_csv(StringIO(csv_input), sep=r'\s*/\s*', engine='python')
        df.columns = ["Question", "Answer 1", "Answer 2", "Answer 3", "Answer 4", "Time", "Correct"]
        
        st.write("Here is a preview of your data (before shuffling for Excel):")
        st.write(df)
        
        # Excel (Shuffled Answers) with updated label
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="Download Kahoot Format (Excel)",
            data=excel_data,
            file_name="table_shuffled.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Add Hyperlink below the Kahoot button
        st.markdown(
            "[Step by Step Kahoot-Import](https://tools.fobizz.com/website/public_pages/66958a17-ad70-45eb-b9c6-30661f0c24ed?token=32367ca42998d30f5ae47692cfee4bda)",
            unsafe_allow_html=True
        )
        
        # LMS Format with updated label
        lms_data = convert_to_lms_format(df)
        st.download_button(
            label="Download OLAT Format (txt)",
            data=lms_data,
            file_name="OLAT_import.txt",
            mime="text/plain"
        )

                # Add Hyperlink below the Kahoot button
        st.markdown(
            "[Step by Step OLAT-Import](https://tools.fobizz.com/website/public_pages/866fd7a0-d855-4d4c-a5cb-04d598c94172?token=14a6005b8efc206258c09d85bf45c3c7)",
            unsafe_allow_html=True
        )

        # H5P Format with updated label
        h5p_data = convert_to_h5p_format(df)
        st.download_button(
            label="Download H5P Export (txt)",
            data=h5p_data,
            file_name="h5p_export.txt",
            mime="text/plain"
        )
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
