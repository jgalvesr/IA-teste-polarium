from flask import Flask, render_template, request, jsonify
import random
import os

# Simulação da PolariumAPI
class PolariumAPI:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):
        print(f"Simulando login para {self.email}")

    def get_candles(self, symbol="BTCUSD", interval="1m", limit=60):
        candles = []
        base_price = random.uniform(100, 50000)
        for i in range(limit):
            close = base_price + random.uniform(-100, 100)
            candles.append({
                "timestamp": f"2025-07-09T00:{i:02}:00Z",
                "close": round(close, 2)
            })
        return candles

    def place_order(self, symbol, side, amount, type="market"):
        return {
            "symbol": symbol,
            "side": side,
            "amount": amount,
            "type": type,
            "status": "simulated",
        }

# Simulação da IA
class ExtraSuperGPTEnhancer:
    def generate_response(self, prompt):
        closes = [float(s) for s in prompt.split("[")[-1].split("]")[0].split(",")]
        if closes[-1] > closes[0]:
            return "DECISÃO: COMPRAR. O preço subiu."
        elif closes[-1] < closes[0]:
            return "DECISÃO: VENDER. O preço caiu."
        else:
            return "DECISÃO: MANTER. O preço está estável."

app = Flask(__name__)
ai = ExtraSuperGPTEnhancer()

# Login simulado
polarium = PolariumAPI(email=os.getenv("POLARIUM_EMAIL", "teste@exemplo.com"),
                       password=os.getenv("POLARIUM_PASSWORD", "senha123"))
polarium.login()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/candles")
def get_candles():
    symbol = request.args.get("symbol", "BTCUSD")
    interval = request.args.get("interval", "1m")
    candles = polarium.get_candles(symbol=symbol, interval=interval, limit=60)
    closes = [float(c['close']) for c in candles]
    timestamps = [c['timestamp'] for c in candles]
    return jsonify({"timestamps": timestamps, "closes": closes})

@app.route("/api/ia-decision")
def ia_decision():
    symbol = request.args.get("symbol", "BTCUSD")
    interval = request.args.get("interval", "1m")
    candles = polarium.get_candles(symbol=symbol, interval=interval, limit=60)
    closes = [float(c['close']) for c in candles]
    prompt = (
        f"Com base nos últimos 60 fechamentos de {symbol} com intervalo {interval}: {closes}, "
        "a IA deve decidir COMPRAR, VENDER ou MANTER, com raciocínio lógico e técnico."
    )
    result = ai.generate_response(prompt)
    return jsonify({"decision": result})

@app.route("/api/trade", methods=["POST"])
def trade():
    data = request.json
    symbol = data.get("symbol", "BTCUSD")
    side = data.get("side")
    amount = data.get("amount", 10)
    try:
        response = polarium.place_order(symbol=symbol, side=side, amount=amount, type="market")
        return jsonify({"status": "ok", "response": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
