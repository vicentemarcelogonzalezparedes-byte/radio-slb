import streamlit as st
from streamlit_gsheets import GSheetsConnection
import re
import unicodedata

st.set_page_config(page_title="Radio SLB", page_icon="📻")

# --- FILTRO DE SEGURIDAD (Nivel 7) ---
BLOQUEADAS = ["sexo", "droga", "tusi", "insulto", "maraco", "culiao"] 

def blindar(texto):
    if not texto: return ""
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', texto.lower())

# --- CONEXIÓN A LA PLANILLA ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📻 Radio San Luis Beltrán")
st.subheader("Envía tu pedido musical")

with st.form("pedidos", clear_on_submit=True):
    nombre = st.text_input("Tu Nombre y Apellido:")
    curso = st.selectbox("Tu Curso:", ["I° Medio", "II° Medio", "III° Medio", "IV° Medio", "Otro"])
    artista = st.text_input("Artista / Grupo:")
    cancion = st.text_input("Nombre de la Canción:")
    enviar = st.form_submit_button("Enviar a Cabina 🚀")

    if enviar:
        verificacion = blindar(artista + cancion)
        if any(p in verificacion for p in BLOQUEADAS):
            st.error("⚠️ Contenido no permitido por las reglas del colegio.")
        else:
            # Aquí mandamos los datos a Google Sheets
            try:
                # Preparamos la fila con los datos
                datos_nuevos = {"Nombre": nombre, "Curso": curso, "Artista": artista, "Cancion": cancion}
                # Esta línea hace la magia de escribir en tu Excel
                conn.create(data=[datos_nuevos])
                st.success("✅ ¡Pedido enviado! Se guardó en la lista de la radio.")
                st.write(f"Registro: {nombre} ({curso}) pide {cancion}")
            except Exception as e:
                st.warning("Se envió, pero hubo un detalle al guardar. Avisa al técnico.")
                st.write(f"Registro local: {nombre} pide {cancion}")