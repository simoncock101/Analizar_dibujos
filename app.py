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

    /* ================================================
       FONDO PRINCIPAL
       ================================================ */

    .stApp {
        background-color: #ffffff;
    }


    /* ================================================
       TEXTOS PRINCIPALES
       ================================================ */

    .titulo {
        font-size: 40px;
        font-weight: 700;
        color: #202124 !important;
        margin-bottom: 0px;
    }

    .subtitulo {
        font-size: 17px;
        color: #5f6368 !important;
        margin-top: 5px;
        margin-bottom: 30px;
    }

    .seccion {
        font-size: 22px;
        font-weight: 700;
        color: #202124 !important;
        margin-bottom: 5px;
    }

    .descripcion {
        font-size: 14px;
        color: #5f6368 !important;
        margin-bottom: 12px;
    }


    /* ================================================
       PANEL DE INFORMACIÓN DE LA IA
       ================================================ */

    .panel-ia {
        background-color: #f3f4f6;
        border: 1px solid #e1e4e8;
        border-radius: 14px;
        padding: 22px;
        margin-top: 10px;
    }

    .panel-ia-titulo {
        font-size: 16px;
        font-weight: 700;
        color: #202124 !important;
        margin-bottom: 15px;
    }

    .panel-ia-texto {
        font-size: 14px;
        color: #4b5563 !important;
        line-height: 1.7;
    }


    /* ================================================
       CANVAS
       ================================================ */

    div[data-testid="stCustomComponentV1"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }


    /* ================================================
       BOTÓN
       ================================================ */

    .stButton > button {
        border-radius: 10px;
        height: 45px;
        font-size: 15px;
        font-weight: 600;
    }


    /* ================================================
       RESULTADO
       ================================================ */

    .resultado {
        background-color: #f3f4f6;
        border: 1px solid #e1e4e8;
        border-radius: 14px;
        padding: 25px;
        margin-top: 25px;
        color: #202124 !important;
    }


    /* ================================================
       TEXTOS DE STREAMLIT
       ================================================ */

    .stMarkdown,
    .stText,
    p,
    label {
        color: #202124;
    }


    /* ================================================
       INPUT DE API
       ================================================ */

    div[data-baseweb="input"] {
        background-color: #ffffff !important;
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
        min_value=1,
        max_value=20,
        value=5
    )

    stroke_color = st.color_picker(
        "Color del dibujo",
        "#222222"
    )

    st.divider()

    st.subheader("Ideas para dibujar")

    st.write("Una casa")
    st.write("Un celular")
    st.write("Un carro")
    st.write("Una silla")
    st.write("Un animal")
    st.write("Un objeto inventado")


# =========================================================
# COLUMNAS
# =========================================================

col1, col2 = st.columns(
    [1.15, 0.85],
    gap="large"
)


# =========================================================
# COLUMNA IZQUIERDA
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


    # -----------------------------------------------------
    # CANVAS
    # -----------------------------------------------------

    canvas_result = st_canvas(

        fill_color="rgba(255, 255, 255, 0)",

        stroke_width=stroke_width,

        stroke_color=stroke_color,

        background_color="#FFFFFF",

        # IMPORTANTE:
        # Este tamaño ahora cabe dentro de la columna.
        height=350,

        width=560,

        drawing_mode="freedraw",

        display_toolbar=True,

        key="boceto_canvas"

    )


    st.write("")


    # -----------------------------------------------------
    # BOTÓN
    # -----------------------------------------------------

    analizar = st.button(
        "🔍 Interpretar boceto",
        type="primary"
    )


# =========================================================
# COLUMNA DERECHA
# =========================================================

with col2:

    st.markdown(
        '<div class="seccion">Análisis con IA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="descripcion">'
        'La inteligencia artificial analizará el dibujo.'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # API KEY
    # -----------------------------------------------------

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-..."
    )


    st.write("")


    # -----------------------------------------------------
    # TARJETA INFORMATIVA
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="panel-ia">

            <div class="panel-ia-titulo">
                ¿Qué hará la inteligencia artificial?
            </div>

            <div class="panel-ia-texto">

                Identificará el objeto que dibujaste.<br><br>

                Indicará qué tan segura es su interpretación.<br><br>

                Describirá los elementos principales del dibujo.<br><br>

                Propondrá tres posibles usos.<br><br>

                Generará una idea creativa relacionada con el objeto.

            </div>

        </div>
        """,
        unsafe_allow_html=True
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
# ANÁLISIS DEL DIBUJO
# =========================================================

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

        with st.spinner(
            "La inteligencia artificial está interpretando tu dibujo..."
        ):

            try:

                # -----------------------------------------
                # Convertir canvas en imagen
                # -----------------------------------------

                input_numpy_array = np.array(
                    canvas_result.image_data
                )

                input_image = Image.fromarray(
                    input_numpy_array.astype("uint8"),
                    "RGBA"
                )

                image_path = "boceto_usuario.png"

                input_image.save(
                    image_path
                )


                # -----------------------------------------
                # Convertir imagen a Base64
                # -----------------------------------------

                base64_image = encode_image_to_base64(
                    image_path
                )


                # -----------------------------------------
                # Cliente OpenAI
                # -----------------------------------------

                client = OpenAI(
                    api_key=api_key
                )


                # -----------------------------------------
                # Prompt
                # -----------------------------------------

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


                # -----------------------------------------
                # Solicitud
                # -----------------------------------------

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


                # -----------------------------------------
                # Resultado
                # -----------------------------------------

                resultado = response.choices[
                    0
                ].message.content


                st.markdown(
                    '<div class="resultado">',
                    unsafe_allow_html=True
                )

                st.subheader(
                    "Resultado del análisis"
                )

                st.markdown(
                    resultado
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            except Exception as e:

                st.error(
                    f"Ocurrió un error: {e}"
                )


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.divider()

st.caption(
    "Boceto IA · Interpretación de dibujos mediante inteligencia artificial"
)
