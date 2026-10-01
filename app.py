import os
import base64
import streamlit as st
import numpy as np
from PIL import Image
from openai import OpenAI
from streamlit_drawable_canvas import st_canvas


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Boceto IA",
    page_icon="✏️",
    layout="wide"
)


# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

    .stApp {
        background-color: #f5f6f8;
    }

    .titulo {
        font-size: 40px;
        font-weight: 700;
        color: #202124;
        margin-bottom: 0px;
    }

    .subtitulo {
        font-size: 17px;
        color: #6b7280;
        margin-top: 5px;
        margin-bottom: 30px;
    }

    .seccion {
        font-size: 22px;
        font-weight: 650;
        color: #202124;
        margin-bottom: 5px;
    }

    .descripcion {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 12px;
    }

    .resultado {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #e1e4e8;
        margin-top: 25px;
    }

    .stButton > button {
        width: 100%;
        height: 46px;
        border-radius: 10px;
        font-size: 15px;
        font-weight: 600;
    }

    /* Hace que el espacio exterior del componente sea blanco */
    iframe {
        background-color: white !important;
        border-radius: 12px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    '<div class="titulo">✏️ Boceto IA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Dibuja una idea y deja que la inteligencia artificial la interprete.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# BARRA LATERAL
# =========================================================

with st.sidebar:

    st.header("⚙️ Configuración")

    st.write(
        "Personaliza tu tablero antes de comenzar."
    )

    st.divider()

    stroke_width = st.slider(
        "Tamaño del pincel",
        1,
        20,
        5
    )

    stroke_color = st.color_picker(
        "Color del dibujo",
        "#222222"
    )

    st.divider()

    st.subheader("💡 Ideas para dibujar")

    st.write("🏠 Una casa")
    st.write("📱 Un celular")
    st.write("🚗 Un carro")
    st.write("🪑 Una silla")
    st.write("🐶 Un animal")
    st.write("🚀 Un objeto inventado")


# =========================================================
# COLUMNAS
# =========================================================

col1, col2 = st.columns(
    [1.2, 0.8],
    gap="large"
)


# =========================================================
# TABLERO
# =========================================================

with col1:

    st.markdown(
        '<div class="seccion">🎨 Tu boceto</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="descripcion">'
        'Dibuja cualquier objeto utilizando el mouse o trackpad.'
        '</div>',
        unsafe_allow_html=True
    )

    canvas_result = st_canvas(

        fill_color="rgba(255, 255, 255, 0)",

        stroke_width=stroke_width,

        stroke_color=stroke_color,

        background_color="#FFFFFF",

        height=400,

        width=650,

        drawing_mode="freedraw",

        display_toolbar=True,

        key="boceto_canvas"
    )

    st.write("")

    analizar = st.button(
        "🔍 Interpretar boceto",
        type="primary"
    )


# =========================================================
# PANEL DE IA
# =========================================================

with col2:

    st.markdown(
        '<div class="seccion">🤖 Análisis con IA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="descripcion">'
        'La inteligencia artificial analizará tu dibujo.'
        '</div>',
        unsafe_allow_html=True
    )

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-..."
    )

    st.write("")

    st.info(
        "Dibuja un objeto en el tablero y presiona "
        "\"Interpretar boceto\"."
    )

    st.write("")

    st.markdown(
        """
        **La IA intentará:**

        🔎 Identificar el objeto

        📊 Indicar su nivel de seguridad

        📝 Describir el dibujo

        💡 Proponer usos

        🚀 Generar una idea creativa
        """
    )


# =========================================================
# FUNCIÓN BASE64
# =========================================================

def encode_image_to_base64(image_path):

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# =========================================================
# ANÁLISIS
# =========================================================

if analizar:

    if not api_key:

        st.warning(
            "⚠️ Primero debes ingresar tu API Key."
        )

    elif canvas_result.image_data is None:

        st.warning(
            "⚠️ Primero realiza un dibujo en el tablero."
        )

    else:

        with st.spinner(
            "🤖 La inteligencia artificial está interpretando tu dibujo..."
        ):

            try:

                input_numpy_array = np.array(
                    canvas_result.image_data
                )

                input_image = Image.fromarray(
                    input_numpy_array.astype("uint8"),
                    "RGBA"
                )

                image_path = "boceto_usuario.png"

                input_image.save(image_path)

                base64_image = encode_image_to_base64(
                    image_path
                )

                client = OpenAI(
                    api_key=api_key
                )

                prompt = """
                Analiza el boceto realizado por el usuario.

                El dibujo puede ser sencillo, incompleto
                o poco preciso.

                Responde en español utilizando esta estructura:

                OBJETO IDENTIFICADO:
                ¿Qué objeto crees que representa?

                SEGURIDAD:
                Indica Bajo, Medio o Alto.

                DESCRIPCIÓN:
                Describe brevemente los elementos visibles.

                POSIBLES USOS:
                Propón 3 posibles usos para ese objeto.

                IDEA CREATIVA:
                Propón una idea interesante para transformar,
                mejorar o utilizar ese objeto.

                Si el dibujo es demasiado ambiguo,
                indícalo claramente.
                """

                response = client.chat.completions.create(

                    model="gpt-4o-mini",

                    messages=[
                        {
                            "role": "user",

                            "content": [

                                {
                                    "type": "text",
                                    "text": prompt
                                },

                                {
                                    "type": "image_url",

                                    "image_url": {
                                        "url":
                                        f"data:image/png;base64,{base64_image}"
                                    }
                                }

                            ]
                        }
                    ],

                    max_tokens=500
                )

                resultado = response.choices[
                    0
                ].message.content

                st.markdown(
                    '<div class="resultado">',
                    unsafe_allow_html=True
                )

                st.subheader("✨ Resultado")

                st.markdown(resultado)

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(
                    f"❌ Ocurrió un error: {e}"
                )


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.divider()

st.caption(
    "Boceto IA · Interpretación de dibujos mediante inteligencia artificial"
)
