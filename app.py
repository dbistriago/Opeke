import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.title("🧱 Nacrt zida od opeka 19×19 cm")

# Unosi
sirina = st.number_input("Širina zida (cm)", min_value=20.0, value=190.0)
visina = st.number_input("Visina zida (cm)", min_value=20.0, value=240.0)
fuga = st.number_input("Debljina fuge (cm)", min_value=0.0, value=1.0)
boja = st.color_picker("Boja opeke", "#D35400")

st.subheader("Otvori (opcionalno)")
broj_otvora = st.number_input("Broj otvora", min_value=0, max_value=10, value=0)

otvori = []
for i in range(broj_otvora):
    st.markdown(f"### Otvor {i+1}")
    w = st.number_input(f"Širina {i+1}. otvora (cm)", value=80.0, key=f"w{i}")
    h = st.number_input(f"Visina {i+1}. otvora (cm)", value=120.0, key=f"h{i}")
    x = st.number_input(f"Pozicija od lijevog ruba {i+1}. otvora (cm)", value=10.0, key=f"x{i}")
    y = st.number_input(f"Pozicija od vrha {i+1}. otvora (cm)", value=10.0, key=f"y{i}")
    otvori.append((x, y, w, h))

# Dimenzije cigle
BRICK_W = 19
BRICK_H = 19

# Zid s fugama
CW = BRICK_W + fuga
CH = BRICK_H + fuga

# Broj cigli koje stanu cijele
bw = int(sirina // CW)
bh = int(visina // CH)

# ➤ DODANO: prikaz broja opeka
ukupno = bw * bh
st.write(f"**Broj opeka u širinu:** {bw}")
st.write(f"**Broj opeka u visinu:** {bh}")
st.write(f"**Ukupan broj opeka:** {ukupno}")

fig, ax = plt.subplots(figsize=(12, 8))

# Crtanje opeka
for j in range(bh):
    pomak = 0  # sve cigle poravnate, nema pomaka
    for i in range(bw):  # samo cigle koje stanu cijele
        x = i * CW + pomak
        y = j * CH
        # preskoči cigle koje upadaju u otvor
        skip = False
        for (ox, oy, ow, oh) in otvori:
            if ox <= x <= ox + ow and oy <= y <= oy + oh:
                skip = True
                break
        if skip:
            continue

        rect = patches.Rectangle((x, y), BRICK_W, BRICK_H,
                                 edgecolor='black', facecolor=boja)
        ax.add_patch(rect)

# Crtanje otvora
for (ox, oy, ow, oh) in otvori:
    rect = patches.Rectangle((ox, oy), ow, oh,
                             edgecolor='blue', facecolor='none', linewidth=2)
    ax.add_patch(rect)
    ax.text(ox + ow/2, oy + oh/2, "OTVOR", ha='center', va='center', color='blue')

# Tehničke kote
ax.annotate(f"{sirina} cm", xy=(0, -5), xytext=(sirina/2, -20),
            ha='center', arrowprops=dict(arrowstyle='<->'))
ax.annotate(f"{visina} cm", xy=(-5, 0), xytext=(-20, visina/2),
            va='center', rotation=90, arrowprops=dict(arrowstyle='<->'))

ax.set_xlim(0, sirina)
ax.set_ylim(0, visina)
ax.invert_yaxis()
ax.set_aspect('equal')
plt.tight_layout()

st.pyplot(fig)

# Spremanje
plt.savefig("zid.png", dpi=300)
plt.savefig("zid.pdf")

st.success("Slika spremljena kao 'zid.png' i 'zid.pdf'.")
st.download_button("⬇️ Preuzmi PNG", open("zid.png", "rb"), "zid.png")
st.download_button("⬇️ Preuzmi PDF", open("zid.pdf", "rb"), "zid.pdf")
