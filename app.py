import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("Kalkulator opeka i cijene")

# --- File uploader ---
uploaded_file = st.file_uploader("Učitaj CSV datoteku", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col=0, decimal=',')
    st.write("Učitana tablica:")
    st.dataframe(df)

    # --- Pretvorba cijena u float ---
    df_float = df.copy()
    for col in df.columns:
        if col != 'opeka':
            df_float[col] = df[col].astype(str).str.replace('€','').str.replace(',','.').astype(float)

    # --- Unos dimenzija otvora ---
    širina_otvora = st.number_input("Širina otvora (m)", min_value=0.0)
    visina_otvora = st.number_input("Visina otvora (m)", min_value=0.0)

    if st.button("Izračunaj opeke i prikaži tablicu"):

        # Pretvaranje indeksa i kolona u float
        dostupne_visine = np.array([float(i) for i in df_float.index])
        dostupne_širine = np.array([float(c) for c in df_float.columns if c != 'opeka'])

        # --- Broj opeka po visini i širini ---
        visina_opeka = max([v for v in dostupne_visine if v <= visina_otvora], dostupne_visine.min())
        širina_opeka = max([s for s in dostupne_širine if s <= širina_otvora], dostupne_širine.min())

        red = df_float.loc[str(visina_opeka)]
        broj_opeka_visina = math.ceil(visina_otvora / visina_opeka * red['opeka'])

        # Interpolacija cijene po širini
        š1 = max([s for s in dostupne_širine if s <= širina_otvora])
        š2 = min([s for s in dostupne_širine if s >= širina_otvora])

        cijena1 = red[str(š1)]
        cijena2 = red[str(š2)]
        t = (širina_otvora - š1) / max(š2 - š1, 1e-6)
        cijena_interp = (1-t)*cijena1 + t*cijena2

        # Broj opeka po širini
        broj_opeka_širina = math.ceil(širina_otvora / širina_opeka)

        # --- Kreiranje tablice opeka ---
        tablica_opeka = []
        redni_broj = 1
        for i in range(broj_opeka_visina):
            for j in range(broj_opeka_širina):
                tablica_opeka.append({
                    "Redni broj": redni_broj,
                    "Red": i+1,
                    "Kolona": j+1,
                    "Širina (m)": širina_opeka,
                    "Visina (m)": visina_opeka,
                    "Cijena (€)": cijena_interp / broj_opeka_širina
                })
                redni_broj += 1

        df_opeka = pd.DataFrame(tablica_opeka)
        st.write("Tablica svih opeka za otvor:")
        st.dataframe(df_opeka)

        # --- Vizualizacija ---
        fig, ax = plt.subplots(figsize=(6,6))
        for index, row in df_opeka.iterrows():
            rect = plt.Rectangle(
                ((row["Kolona"]-1)*row["Širina (m)"], (row["Red"]-1)*row["Visina (m)"]),
                row["Širina (m)"], row["Visina (m)"],
                edgecolor='brown', facecolor='orange', linewidth=1
            )
            ax.add_patch(rect)
        ax.set_xlim(0, širina_otvora)
        ax.set_ylim(0, visina_otvora)
        ax.set_aspect('equal')
        ax.set_xlabel("Širina (m)")
        ax.set_ylabel("Visina (m)")
        ax.set_title("Vizualizacija otvora s opekom")
        st.pyplot(fig)

        # --- Rezultati ---
        st.write(f"Ukupno opeka: {broj_opeka_visina * broj_opeka_širina}")
        st.write(f"Ukupna cijena otvora: {cijena_interp:.2f} €")
