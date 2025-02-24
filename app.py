import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO, BytesIO
from zipfile import ZipFile

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
        
        lms_format = (
            f"Typ\tSC\n"
            f"Level\tWissen\n"
            f"Title\t{question[:50]}...\n"
            f"Question\t{question}\n"
            f"Points\t1\n"
            f"1\t{correct_answer}\n" +
            "\n".join([f"-0.5\t{answer}" for answer in incorrect_answers])
        )
        lms_output.append(lms_format)
    
    return "\n\n".join(lms_output)

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

def create_bulk_zip(excel_data, lms_data, h5p_data):
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, "w") as zip_file:
        zip_file.writestr("table_shuffled.xlsx", excel_data)
        zip_file.writestr("OLAT_import.txt", lms_data)
        zip_file.writestr("h5p_export.txt", h5p_data)
    zip_buffer.seek(0)
    return zip_buffer.read()

st.title("Table to Excel for Kahoot-Import")
st.write("Paste your data in the text area below. Use slash (/) to separate columns and new lines to separate rows. Use this [customGPT](https://chatgpt.com/g/g-hKBP1U4Ks-kahoot-streamlit) first to generate the data")

csv_input = st.text_area("Input your data here:", height=300)

# Ensure persistent state variables for the outputs.
if "converted" not in st.session_state:
    st.session_state.converted = False
if "excel_data" not in st.session_state:
    st.session_state.excel_data = None
if "lms_data" not in st.session_state:
    st.session_state.lms_data = None
if "h5p_data" not in st.session_state:
    st.session_state.h5p_data = None
if "zip_data" not in st.session_state:
    st.session_state.zip_data = None

if st.button("Convert and Download"):
    try:
        # Substitute 'ß' with 'ss' in the input
        csv_input_clean = csv_input.replace("ß", "ss")
        
        # Adjusted separator to handle spaces around slash
        df = pd.read_csv(StringIO(csv_input_clean), sep=r'\s*/\s*', engine='python')
        df.columns = ["Question", "Answer 1", "Answer 2", "Answer 3", "Answer 4", "Time", "Correct"]
        
        st.write("Here is a preview of your data (before shuffling for Excel):")
        st.write(df)
        
        # Generate outputs
        excel_data = convert_df_to_excel(df)
        lms_data = convert_to_lms_format(df)
        h5p_data = convert_to_h5p_format(df)
        zip_data = create_bulk_zip(excel_data, lms_data, h5p_data)
        
        # Save outputs to session state for persistence
        st.session_state.excel_data = excel_data
        st.session_state.lms_data = lms_data
        st.session_state.h5p_data = h5p_data
        st.session_state.zip_data = zip_data
        st.session_state.converted = True

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display download options if conversion has been completed.
if st.session_state.converted:
    st.download_button(
        label="Download Kahoot Format (Excel)",
        data=st.session_state.excel_data,
        file_name="table_shuffled.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.markdown(
        "[Step by Step Kahoot-Import](https://tools.fobizz.com/website/public_pages/66958a17-ad70-45eb-b9c6-30661f0c24ed?token=32367ca42998d30f5ae47692cfee4bda)",
        unsafe_allow_html=True
    )
    st.download_button(
        label="Download OLAT Format (txt)",
        data=st.session_state.lms_data,
        file_name="OLAT_import.txt",
        mime="text/plain"
    )
    st.markdown(
        "[Step by Step OLAT-Import](https://tools.fobizz.com/website/public_pages/866fd7a0-d855-4d4c-a5cb-04d598c94172?token=14a6005b8efc206258c09d85bf45c3c7)",
        unsafe_allow_html=True
    )
    st.download_button(
        label="Download H5P Export (txt)",
        data=st.session_state.h5p_data,
        file_name="h5p_export.txt",
        mime="text/plain"
    )
    st.download_button(
        label="Download All Files (ZIP)",
        data=st.session_state.zip_data,
        file_name="all_files.zip",
        mime="application/zip"
    )
