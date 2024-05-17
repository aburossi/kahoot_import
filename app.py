import streamlit as st
import pandas as pd
from io import BytesIO

# Sample table data
data = {
    "ge": ["Was ist der Hauptfaktor, der den Auftrieb in Gasen bestimmt?", "Welches Gesetz beschreibt den Auftrieb in Gasen?"],
    "Antwort 1": ["Die Temperatur des Gases", "Newtons erstes Gesetz"],
    "Antwort 2": ["Das Volumen des Gases", "Archimedisches Prinzip"],
    "Antwort 3": ["Die Dichte des Gases", "Boyles Gesetz"],
    "Antwort 4": ["Die Höhe über dem Meeresspiegel", "Charles' Gesetz"],
    "Korrekte Antwort": ["C", "B"],
    "Zeit (Sekunden)": [20, 20]
}

# Create DataFrame
df = pd.DataFrame(data)

# Streamlit UI
st.title("Table to Excel Converter")

st.write("Here is the sample table data:")
st.write(df)

# Function to convert DataFrame to Excel
@st.cache
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
    processed_data = output.getvalue()
    return processed_data

# Convert and provide download link
if st.button("Generate and Download Excel"):
    excel_data = convert_df_to_excel(df)
    st.download_button(
        label="Download Excel",
        data=excel_data,
        file_name="table.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
