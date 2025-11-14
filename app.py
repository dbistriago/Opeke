import streamlit as st
import pandas as pd

st.title("Izračun opeka i cijene")

uploaded_file = st.file_uploader("Učitaj CSV datoteku", type="csv")

if uploaded_file is not None:
    try:
        # Učitaj CSV, header je treći red (index 2)
        df = pd.read_csv(
            uploaded_file,
            decimal=',',
            header=2,            # koristi treći red kao zaglavlje
            encoding='cp1250',
            on_bad_lines='skip'
        )

        # Pretvori cijene u float
        for col in df.columns[2:]:
            df[col] = df[col].astype(str).str.replace('€','').str.replace(',','.').astype(float)

        df.set_index('visina', inplace=True)

        st.write("Tablica učitana:")
        st.dataframe(df)

        # Unos visine i širine
        visina_input = st.number_input("Unesi visinu:", value=float(df.index[0]))
        sirina_input = st.selectbox("Odaberi širinu:", df.columns[2:])
