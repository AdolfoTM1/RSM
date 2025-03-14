import streamlit as st
import xml.etree.ElementTree as ET
import datetime

# Función para crear el XML basado en las entradas del usuario
def create_xml(data):
    root = ET.Element("Operacion")
    
    operaciones = ET.SubElement(root, "Operaciones_de_compra_yX85Xo_venta_de_bienes_inmuebles")

    for key, value in data.items():
        child = ET.SubElement(operaciones, key)
        child.text = str(value) if value is not None else ""

    return ET.tostring(root, encoding='unicode')

# Título de la aplicación
st.title("Generador de XML para Operaciones de Inmuebles")

# Formulario para los campos del XML
with st.form(key='xml_form'):
    # Campos de entrada
    fecha_operacion = st.date_input("Fecha de la operación", datetime.date.today())
    tipo_moneda_origen = st.selectbox("Tipo de moneda de origen", ["Elegir...", "Peso Argentino", "Otro"])
    monto_total_moneda_origen = st.number_input("Monto total de la operación en moneda de origen", min_value=0)
    nomenclatura_catastral = st.text_input("Nomenclatura catastral del inmueble transferido")
    provincia_inmueble = st.selectbox("Provincia del inmueble", [
        "CABA", "Buenos Aires", "Catamarca", "Córdoba", "Corrientes", "Chaco", 
        "Chubut", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja", 
        "Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan", 
        "San Luis", "Santa Cruz", "Santa Fé", "Santiago Del Estero", "Tucumán", "Tierra del Fuego"
    ])
    localidad_inmueble = st.text_input("Localidad del inmueble")
    calle_inmueble = st.text_input("Calle del inmueble")
    numero_inmueble = st.text_input("Número del inmueble")
    
    # Botón para enviar el formulario
    submit_button = st.form_submit_button("Crear XML")

    if submit_button:
        # Recopilar los datos en un diccionario
        data = {
            "Fecha_de_la_operaci93n": fecha_operacion.isoformat(),
            "Tipo_de_moneda_de_origen": tipo_moneda_origen,
            "Monto_total_de_la_operaci93n_en_moneda_de_origen": monto_total_moneda_origen,
            "Nomenclatura_catastral_o_matr92cula_del_inmueble_transferido": nomenclatura_catastral,
            "Provincia_del_inmueble": provincia_inmueble,
            "Localidad_del_inmueble": localidad_inmueble,
            "Calle_del_inmueble": calle_inmueble,
            "N94mero_del_inmueble": numero_inmueble,
        }

        # Crear el XML
        xml_output = create_xml(data)

        # Mostrar el XML generado
        st.success("XML generado exitosamente:")
        st.code(xml_output)

        # Opción para descargar el XML como archivo
        st.download_button("Descargar XML", xml_output, file_name="output.xml", mime="application/xml")
