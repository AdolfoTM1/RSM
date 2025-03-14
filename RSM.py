import streamlit as st
from lxml import etree
from datetime import datetime

def create_xml(data):
    root = etree.Element("Operacion")
    operaciones = etree.SubElement(root, "Operaciones_de_compra_yX85Xo_venta_de_bienes_inmuebles", Version="1.0")

    # Datos de la operación
    fecha_operacion = etree.SubElement(operaciones, "Fecha_de_la_operaci93n")
    fecha_operacion.text = data["fecha_operacion"].isoformat()

    tipo_moneda_origen = etree.SubElement(operaciones, "Tipo_de_moneda_de_origen")
    tipo_moneda_origen.text = data["tipo_moneda_origen"]

    if data["tipo_moneda_origen"] == "Otro":
        tipo_moneda_extranjera = etree.SubElement(operaciones, "Tipo_de_moneda_extranjera")
        tipo_moneda_extranjera.text = data["tipo_moneda_extranjera"]
        monto_pesos = etree.SubElement(operaciones, "Monto_total_de_la_operaci93n_equivalente_en_Pesos")
        monto_pesos.text = str(data["monto_pesos"])

    monto_total_moneda_origen = etree.SubElement(operaciones, "Monto_total_de_la_operaci93n_en_moneda_de_origen")
    monto_total_moneda_origen.text = str(data["monto_total_moneda_origen"])

    nomenclatura = etree.SubElement(operaciones, "Nomenclatura_catastral_o_matr92cula_del_inmueble_transferido")
    nomenclatura.text = data["nomenclatura"]

    provincia = etree.SubElement(operaciones, "Provincia_del_inmueble")
    provincia.text = data["provincia"]

    localidad = etree.SubElement(operaciones, "Localidad_del_inmueble")
    localidad.text = data["localidad"]

    calle = etree.SubElement(operaciones, "Calle_del_inmueble")
    calle.text = data["calle"]

    numero = etree.SubElement(operaciones, "N94mero_del_inmueble")
    numero.text = data["numero"]

    if data["piso"]:
        piso = etree.SubElement(operaciones, "Piso_del_inmueble")
        piso.text = data["piso"]
    if data["departamento"]:
        departamento = etree.SubElement(operaciones, "Departamento_del_inmueble")
        departamento.text = data["departamento"]
    if data["codigo_postal"]:
        codigo_postal = etree.SubElement(operaciones, "C93digo_postal_del_inmueble")
        codigo_postal.text = data["codigo_postal"]

    #formas de pago
    for forma_pago_data in data["formas_pago"]:
        formas_pago_element = etree.SubElement(operaciones, "FORMAS_DE_PAGO")
        forma_de_pago = etree.SubElement(formas_pago_element, "Forma_de_pago")
        forma_de_pago.text = forma_pago_data["forma_de_pago"]

        if forma_pago_data["forma_de_pago"] == "Activo Virtual":
            tipo_activo_virtual = etree.SubElement(formas_pago_element, "Tipo_de_activo_virtual")
            tipo_activo_virtual.text = forma_pago_data["tipo_activo_virtual"]
        if forma_pago_data["forma_de_pago"] == "Otra":
            otra = etree.SubElement(formas_pago_element, "Otra")
            otra.text = forma_pago_data["otra"]

        tipo_moneda_pago = etree.SubElement(formas_pago_element, "Tipo_de_moneda_de_origen_del_pago")
        tipo_moneda_pago.text = forma_pago_data["tipo_moneda_pago"]
        if forma_pago_data["tipo_moneda_pago"] == "Otro":
            tipo_moneda_extranjera_pago = etree.SubElement(formas_pago_element, "Tipo_de_moneda_extranjera_de_origen_del_pago")
            tipo_moneda_extranjera_pago.text = forma_pago_data["tipo_moneda_extranjera_pago"]
            monto_pesos_pago = etree.SubElement(formas_pago_element, "Monto_Pagado_de_la_operaci93n_equivalente_en_Pesos")
            monto_pesos_pago.text = str(forma_pago_data["monto_pesos_pago"])

        monto_moneda_pago = etree.SubElement(formas_pago_element, "Monto_Pagado_de_la_operaci93n_en_moneda_de_origen")
        monto_moneda_pago.text = str(forma_pago_data["monto_moneda_pago"])

    #generar el resto de los elementos
    #...

    return etree.tostring(root, pretty_print=True, encoding="utf-8").decode("utf-8")

def main():
    st.title("Generador de XML de Operaciones Inmobiliarias")

    # Datos de la operación
    st.header("Datos de la Operación")
    fecha_operacion = st.date_input("Fecha de la operación", datetime.today())
    tipo_moneda_origen = st.selectbox("Tipo de moneda de origen", ["Elegir...", "Peso Argentino", "Otro"])
    tipo_moneda_extranjera = st.text_input("Tipo de moneda extranjera (si aplica)")
    monto_pesos = st.number_input("Monto total en pesos (si aplica)", value=0)
