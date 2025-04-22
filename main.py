import streamlit as st
import pdfplumber

def extract_alarm_data(pdf_file):
    results = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and len(row) >= 4:
                        type_column = row[0]
                        time_column = row[2]
                        condition_column = row[3]

                        if type_column and "Alarm" in type_column:
                            condition_clean = condition_column.replace("\n", " ").strip().lower()
                            if "device does not respond" not in condition_clean:
                                results.append((time_column.strip(), condition_column.strip()))
    return results

st.title("Alarm PDF elemző")

uploaded_file = st.file_uploader("Tölts fel egy PDF fájlt", type="pdf")

if uploaded_file is not None:
    alarms = extract_alarm_data(uploaded_file)
    if alarms:
        st.success(f"{len(alarms)} riasztást találtam:")
        for time, condition in alarms:
            st.text(f"Alarm at {time}, Condition: {condition}")
    else:
        st.info("Nem találtam 'Alarm' eseményt.")