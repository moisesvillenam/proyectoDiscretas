from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Función para calcular la tabla de amortización francesa
def calcular_amortizacion(monto, tasa_interes_anual, periodos):
    n = 12  # Asumimos pagos mensuales
    tasa_mensual = tasa_interes_anual / (n * 100)
    cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** periodos) / ((1 + tasa_mensual) ** periodos - 1)
    
    saldo = monto
    amortizaciones = []
    intereses = []
    saldos = []
    pagos = []

    for i in range(1, periodos + 1):
        interes_periodo = saldo * tasa_mensual
        amortizacion = cuota - interes_periodo
        saldo -= amortizacion

        amortizaciones.append(amortizacion)
        intereses.append(interes_periodo)
        saldos.append(saldo)
        pagos.append(cuota)

    return pagos, intereses, amortizaciones, saldos

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    monto = float(data['monto'])
    tasa_interes_anual = float(data['tasa'])
    periodos = int(data['periodos'])

    pagos, intereses, amortizaciones, saldos = calcular_amortizacion(monto, tasa_interes_anual, periodos)
    
    # Generar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, periodos + 1), amortizaciones, label='Amortización de Capital')
    plt.plot(range(1, periodos + 1), intereses, label='Intereses')
    plt.plot(range(1, periodos + 1), saldos, label='Saldo Remanente')
    plt.xlabel('Periodo')
    plt.ylabel('Monto')
    plt.title('Amortización Francesa')
    plt.legend()
    plt.grid(True)
    
    # Convertir gráfico a imagen base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return jsonify({
        "pagos": pagos,
        "intereses": intereses,
        "amortizaciones": amortizaciones,
        "saldos": saldos,
        "graph_url": f"data:image/png;base64,{graph_url}"
    })

if __name__ == '__main__':
    app.run(debug=True)
