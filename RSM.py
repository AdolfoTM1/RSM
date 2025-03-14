import streamlit as st
from lxml import etree
from datetime import datetime

def create_xml(data):
    root = etree.Element("Operacion")
    operaciones = etree.SubElement(root, "Operaciones_de_compra_yX85Xo_venta_de_bienes_inmuebles", Version="1.0")

    # Fecha de la operación
    fecha_operacion = etree.SubElement(operaciones, "Fecha_de_la_operaci93n")
    fecha_operacion.text = data["fecha_operacion"].isoformat()

    # Tipo de moneda
    tipo_moneda_origen = etree.SubElement(operaciones, "Tipo_de_moneda_de_origen")
    tipo_moneda_origen.text = data["tipo_moneda_origen"]

    # Monto total
    monto_total_moneda_origen = etree.SubElement(operaciones, "Monto_total_de_la_operaci93n_en_moneda_de_origen")
    monto_total_moneda_origen.text = str(data["monto_total_moneda_origen"])

    # Compradores y vendedores (simplificado)
    for persona in data["personas"]:
        persona_element = etree.SubElement(operaciones, "IDENTIFICACI98N_DEL_COMPRADOR_Y_VENDEDOR")
        rol = etree.SubElement(persona_element, "Rol_en_la_Operaci93n88CompradorVendedor")
        rol.text = persona["rol"]
        tipo = etree.SubElement(persona_element, "Tipo_de_Persona88CompradorVendedor")
        tipo.text = persona["tipo"]
        cuit = etree.SubElement(persona_element, "N94mero_de_CUITX85XCUIL88Persona_Humana")
        cuit.text = persona["cuit"]

    return etree.tostring(root, pretty_print=True, encoding="utf-8").decode("utf-8")

def main():
    st.title("Generador de XML de Operaciones Inmobiliarias (Simplificado)")

    # Datos de la operación
    st.header("Datos de la Operación")
    fecha_operacion = st.date_input("Fecha de la operación", datetime.today())
    tipo_moneda_origen = st.selectbox("Tipo de moneda de origen", ["Elegir...", "Peso Argentino", "Otro"])
    monto_total_moneda_origen = st.number_input("Monto total de la operación", value=0)

    # Compradores y vendedores
    st.header("Compradores y Vendedores")
    personas = []
    if st.button("Agregar Comprador/Vendedor"):
        personas.append({"rol": "Comprador", "tipo": "Persona Humana", "cuit": ""})  # Valores iniciales

    for i, persona in enumerate(personas):
        st.subheader(f"Persona {i + 1}")
        persona["rol"] = st.selectbox("Rol", ["Comprador", "Vendedor"], key=f"rol_{i}")
        persona["tipo"] = st.selectbox("Tipo de Persona", ["Persona Humana", "Persona Jurídica"], key=f"tipo_{i}")
        persona["cuit"] = st.text_input("CUIT", key=f"cuit_{i}")

    # Generar y descargar XML
    if st.button("Generar XML"):
        data = {
            "fecha_operacion": fecha_operacion,
            "tipo_moneda_origen": tipo_moneda_origen,
            "monto_total_moneda_origen": monto_total_moneda_origen,
            "personas": personas,
        }
        xml_output = create_xml(data)
        st.download_button(
            label="Descargar XML",
            data=xml_output.encode("utf-8"),
            file_name="operacion.xml",
            mime="application/xml",
        )

if __name__ == "__main__":
    main()
