import streamlit as st
import pandas as pd
from io import BytesIO

# Function to convert DataFrame to Excel
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
    processed_data = output.getvalue()
    return processed_data

# Streamlit UI
st.title("Table to Excel Converter")

st.write("Enter your table data in the text area below. Use tab or comma to separate columns and new lines to separate rows.")
sample_data = """Frage\tAntwort 1\tAntwort 2\tAntwort 3\tAntwort 4\tKorrekte Antwort\tZeit (Sekunden)
Was ist der Hauptfaktor, der den Auftrieb in Gasen bestimmt?\tDie Temperatur des Gases\tDas Volumen des Gases\tDie Dichte des Gases\tDie Höhe über dem Meeresspiegel\tC\t20
Welches Gesetz beschreibt den Auftrieb in Gasen?\tNewtons erstes Gesetz\tArchimedisches Prinzip\tBoyles Gesetz\tCharles' Gesetz\tB\t20
Was passiert mit dem Auftrieb, wenn die Dichte des Gases abnimmt?\tEr nimmt zu\tEr nimmt ab\tEr bleibt gleich\tEr wird negativ\tB\t20
Wie beeinflusst die Temperatur den Auftrieb in einem Gas?\tHöhere Temperatur erhöht die Dichte\tHöhere Temperatur verringert die Dichte\tTemperatur hat keinen Einfluss\tHöhere Temperatur erhöht den Druck ohne Dichteänderung\tB\t20
Welche Rolle spielt der Druck bei der Bestimmung des Auftriebs in Gasen?\tKeine Rolle\tErhöhter Druck verringert den Auftrieb\tVerringerte Druck erhöht den Auftrieb\tDruck ist direkt proportional zum Auftrieb\tD\t20
Wie verhält sich ein Ballon in einem Vakuum bezüglich des Auftriebs?\tEr steigt auf\tEr fällt\tEr bleibt in der gleichen Höhe\tEr explodiert\tB\t20
Warum steigen Heißluftballons auf?\tDie Luft im Ballon ist kälter als die Umgebung\tDie Luft im Ballon ist dichter als die Umgebung\tDie Luft im Ballon ist weniger dicht als die Umgebung\tDer Ballon erzeugt einen Aufwärtsdruck\tC\t20
Was ist für den Auftrieb in einem Gas verantwortlich?\tDie Gravitationskraft des Gases\tDie magnetische Anziehungskraft des Gases\tDer Unterschied in der Dichte zwischen Objekt und Gas\tDie elektrische Ladung des Gases\tC\t20
Wie beeinflusst die Höhe über dem Meeresspiegel den Auftrieb in einem Gas?\tHöhere Höhen erhöhen den Auftrieb\tHöhere Höhen verringern den Auftrieb\tKein Einfluss\tHöhere Höhen erhöhen die Dichte\tB\t20
Welche Aussage über den Auftrieb in Gasen ist falsch?\tAuftrieb ist unabhängig von der Gravitation\tAuftrieb in Gasen kann durch das Archimedische Prinzip erklärt werden\tAuftrieb hängt von der Dichte des Gases ab\tAuftrieb nimmt zu, wenn die Dichte des umgebenden Gases zunimmt\tA\t20
Welcher Faktor beeinflusst den Auftrieb nicht direkt?\tViskosität des Gases\tDichte des Gases\tVolumen des eingetauchten Objekts\tGewicht des eingetauchten Objekts\tA\t20
Kann ein Objekt in einem dichteren Gas mehr Auftrieb erfahren als in einem weniger dichten Gas?\tJa, das ist immer der Fall\tNein, das ist nie der Fall\tJa, aber nur wenn das Objekt weniger dicht als das Gas ist\tNein, es hängt von der Form des Objekts ab\tC\t20"""

table_input = st.text_area("Input your table data here:", value=sample_data, height=300)

if st.button("Convert and Download Excel"):
    try:
        df = pd.read_csv(pd.compat.StringIO(table_input), sep='\t')
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name="table.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
