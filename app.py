import os
import base64
import streamlit as st
import numpy as np
from PIL import Image
from openai import OpenAI
from streamlit_drawable_canvas import st_canvas


# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------

st.set_page_config(
    page_title="Boceto IA",
    page_icon="✏️",
    layout="wide"
)


# ---------------------------------------------------------
# ESTILOS VISUALES
# ---------------------------------------------------------

st.markdown("""
<style>

    .stApp {
        background-color: #f4f5f7;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #202124;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 25px;
    }

    .info-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        margin-bottom: 20px;
    }

    .result-box {
        background-color: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #dddddd;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.06);
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# TÍTULO
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">✏️ Boceto IA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Dibuja una idea y deja que la inteligencia artificial la interprete.'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Configuración")

    st.write(
        "Usa el tablero para realizar un dibujo sencillo. "
        "La inteligencia artificial intentará reconocerlo."
    )

    st.divider()

    stroke_width = st.slider(
        "Tamaño del pincel",
        min_value=1,
        max_value=30,
        value=5
    )

    stroke_color = st.color_picker(
        "Color del dibujo",
        "#222222"
    )

    st.divider()

    st.subheader("💡 Ejemplos")

    st.write("• Una casa")
    st.write("• Un celular")
    st.write("• Un carro")
    st.write("• Una silla")
    st.write("• Un animal")
    st.write("• Un objeto inventado")


# ---------------------------------------------------------
# FUNCIÓN PARA CONVERTIR LA IMAGEN
# ---------------------------------------------------------

def encode_image_to_base64(image_path):

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# ---------------------------------------------------------
# TABLERO
# ---------------------------------------------------------

col1, col2 = st.columns([1.2, 1])

with col1:

    st.markdown(
        '<div class="info-box">',
        unsafe_allow_html=True
    )

    st.subheader("🎨 Tu boceto")

    st.write(
        "Dibuja un objeto utilizando el mouse o el trackpad."
    )

    canvas_result = st_canvas(

        fill_color="rgba(255, 255, 255, 0)",

        stroke_width=stroke_width,

        stroke_color=stroke_color,

        background_color="#FFFFFF",

        height=400,

        width=600,

        drawing_mode="freedraw",

        key="boceto_canvas"

    )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# API KEY
# ---------------------------------------------------------

with col2:

    st.markdown(
        '<div class="info-box">',
        unsafe_allow_html=True
    )

    st.subheader("🔑 Conexión con IA")

    api_key = st.text_input(
        "Ingresa tu API Key",
        type="password",
        placeholder="sk-..."
    )

    st.write(
        "La clave se utiliza para enviar el dibujo "
        "al modelo de inteligencia artificial."
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# BOTÓN DE ANÁLISIS
# ---------------------------------------------------------

analizar = st.button(
    "🔍 INTERPRETAR MI BOCETO",
    type="primary"
)


# ---------------------------------------------------------
# ANÁLISIS DEL DIBUJO
# ---------------------------------------------------------

if analizar:

    if not api_key:

        st.warning(
            "Primero debes ingresar tu API Key."
        )

    elif canvas_result.image_data is None:

        st.warning(
            "Primero realiza un dibujo en el tablero."
        )

    else:

        with st.spinner("La IA está interpretando tu dibujo..."):

            try:

                # Convertir el dibujo a imagen
                input_numpy_array = np.array(
                    canvas_result.image_data
                )

                input_image = Image.fromarray(
                    input_numpy_array.astype("uint8"),
                    "RGBA"
                )

                # Guardar imagen temporal
                image_path = "boceto_usuario.png"

                input_image.save(image_path)

                # Convertir imagen a Base64
                base64_image = encode_image_to_base64(
                    image_path
                )

                # Crear cliente OpenAI
                client = OpenAI(
                    api_key=api_key
                )

                # Prompt para la nueva función
                prompt = """
                Analiza el boceto que aparece en la imagen.

                La persona realizó el dibujo a mano y puede ser
                sencillo, incompleto o poco preciso.

                Responde en español y utiliza exactamente esta estructura:

                OBJETO IDENTIFICADO:
                Indica qué objeto crees que representa el dibujo.

                NIVEL DE SEGURIDAD:
                Indica qué tan seguro estás de tu interpretación,
                usando Bajo, Medio o Alto.

                DESCRIPCIÓN:
                Explica brevemente qué elementos observas en el dibujo.

                POSIBLES USOS:
                Propón 3 posibles usos que podría tener el objeto.

                IDEA CREATIVA:
                Propón una idea interesante para transformar o mejorar
                el objeto.

                No inventes detalles que claramente no aparecen.
                Si el dibujo es demasiado ambiguo, dilo.
                """

                # Solicitud al modelo
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

                # -------------------------------------------------
                # MOSTRAR RESULTADO
                # -------------------------------------------------

                st.markdown(
                    '<div class="result-box">',
                    unsafe_allow_html=True
                )

                st.subheader("🤖 Interpretación de la IA")

                st.markdown(resultado)

                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:

                st.error(
                    f"Ocurrió un error al analizar el dibujo: {e}"
                )


# ---------------------------------------------------------
# INFORMACIÓN INFERIOR
# ---------------------------------------------------------

st.divider()

st.caption(
    "Boceto IA — Aplicación experimental de interpretación "
    "de dibujos mediante inteligencia artificial."
)
