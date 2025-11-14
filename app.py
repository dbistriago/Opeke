import streamlit as st
import pandas as pd

st.title("Izračun opeka i cijene")

# Upload CSV
uploaded_file = st.file_uploader("Učitaj CSV datoteku", type="csv")

if uploaded_file is not None:
    # Učitavanje CSV-a
    df = pd.read_csv(uploaded_file, decimal=',', skiprows=[1])  # preskoči drugi red koji je '.'

    # Pretvori cijene iz stringa u float
    for col in df.columns[2:]:
        df[col] = df[col].astype(str).str.replace('€','').str.replace(',','.').astype(float)

    df.set_index('visina', inplace=True)

    st.write("Tablica učitana:")
    st.dataframe(df)

    # Unos visine i širine
    visina_input = st.number_input("Unesi visinu:", value=float(df.index[0]))
    sirina_input = st.selectbox("Odaberi širinu:", df.columns[2:])  # kolone s cijenama

    if st.button("Izračunaj"):
        try:
            cijena = df[sirina_input].loc[visina_input]
            broj_opeka = df['opeka'].loc[visina_input]
            ukupno = cijena * broj_opeka

            st.success(f"Broj opeka: {broj_opeka}")
            st.success(f"Cijena po opeki: {cijena:.2f} €")
            st.success(f"Ukupna cijena: {ukupno:.2f} €")
        except KeyError:
            st.error("Nepostojeća kombinacija visine i širine!")
