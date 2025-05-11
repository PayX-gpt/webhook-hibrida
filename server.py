
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NICCOCHAT_WEBHOOK_URL = "https://seu-endpoint-do-niccochat.com/send"  # <- você colocará aqui depois

@app.route("/webhook-coldmart", methods=["POST"])
def receber_webhook():
    data = request.json

    # Verifica se status da transação é aprovado
    status = data.get("transaction", {}).get("status", "")
    if status not in ["PAID", "APPROVED", "CONFIRMED"]:
        return jsonify({"msg": "Pagamento ainda não confirmado, ignorado."}), 200

    email = data.get("client", {}).get("email")
    nome = data.get("client", {}).get("name")
    telefone = data.get("client", {}).get("phone")

    if not email or not telefone:
        return jsonify({"msg": "Faltando email ou telefone"}), 400

    # Gera senha padrão
    senha = "senha1234"

    # Monta link de acesso automático
    link_acesso = f"https://acesso-hibrida.v0.dev/?email={email}&senha={senha}"

    # Mensagem a ser enviada no WhatsApp
    mensagem = f"Olá {nome}, seu acesso à Plataforma Híbrida foi liberado!\n\nClique no link abaixo para entrar automaticamente, sem precisar digitar nada:\n{link_acesso}\n\nCaso não consiga acessar, fale com nosso suporte."

    # Envio para o NiccoChat (exemplo - você colocará o real depois)
    payload_nicco = {
        "phone": telefone,
        "message": mensagem
    }

    # Aqui você ativa quando tiver o endpoint real do NiccoChat:
    # requests.post(NICCOCHAT_WEBHOOK_URL, json=payload_nicco)

    return jsonify({"msg": "Link gerado e mensagem pronta para envio", "link": link_acesso}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
