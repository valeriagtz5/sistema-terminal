
from flask import Flask, request, jsonify
import random
import uuid
import os
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

BANCOS = [
    "BBVA",
    "BANAMEX",
    "SANTANDER",
    "HSBC",
    "BANORTE"
]

TIPOS_TARJETA = [
    "DEBITO",
    "CREDITO"
]


@app.route("/cobrarTarjeta", methods=["POST"])
def cobrar_tarjeta():
    data = request.json

    if data is None:
        return jsonify({
            "aprobado": False,
            "mensaje": "Solicitud inválida"
        }), 400

    monto = data.get("monto")

    if monto is None or monto <= 0:
        return jsonify({
            "aprobado": False,
            "mensaje": "Monto inválido"
        }), 400

    banco = random.choice(BANCOS)
    tipo_tarjeta = random.choice(TIPOS_TARJETA)
    ultimos4 = str(random.randint(1000, 9999))
    numero_autorizacion = str(uuid.uuid4())[:8].upper()

    return jsonify({
        "aprobado": True,
        "mensaje": "Pago aprobado por la terminal bancaria",
        "monto": monto,
        "numeroAutorizacion": numero_autorizacion,
        "ultimos4Digitos": ultimos4,
        "banco": banco,
        "tipoTarjeta": tipo_tarjeta
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "OK",
        "servicio": "Terminal bancaria simulada"
    })

@app.route("/cobrarCodi", methods=["POST"])
def cobrar_codi():

    data = request.json

    monto = data.get("monto")

    folio = str(random.randint(10000000, 99999999))

    contenido_qr = f"""
    CODI
    MONTO:{monto}
    FOLIO:{folio}
    """

    qr = qrcode.make(contenido_qr)

    buffer = BytesIO()

    qr.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return jsonify({
        "aprobado": True,
        "mensaje": "Pago CoDi aprobado",
        "folio": folio,
        "qrBase64": qr_base64
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)
