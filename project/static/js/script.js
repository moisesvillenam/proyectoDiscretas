document.getElementById('amortizacion-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const monto = document.getElementById('monto').value;
    const tasa = document.getElementById('tasa').value;
    const periodos = document.getElementById('periodos').value;

    fetch('/calcular', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            monto: monto,
            tasa: tasa,
            periodos: periodos
        }),
    })
    .then(response => response.json())
    .then(data => {
        const tbody = document.querySelector('#tabla-resultados tbody');
        tbody.innerHTML = '';

        data.pagos.forEach((pago, index) => {
            const row = document.createElement('tr');

            const periodoCell = document.createElement('td');
            periodoCell.textContent = index + 1;
            row.appendChild(periodoCell);

            const cuotaCell = document.createElement('td');
            cuotaCell.textContent = pago.toFixed(2);
            row.appendChild(cuotaCell);

            const interesCell = document.createElement('td');
            interesCell.textContent = data.intereses[index].toFixed(2);
            row.appendChild(interesCell);

            const amortizacionCell = document.createElement('td');
            amortizacionCell.textContent = data.amortizaciones[index].toFixed(2);
            row.appendChild(amortizacionCell);

            const saldoCell = document.createElement('td');
            saldoCell.textContent = data.saldos[index].toFixed(2);
            row.appendChild(saldoCell);

            tbody.appendChild(row);
        });

        document.getElementById('grafico').src = data.graph_url;
    })
    .catch(error => console.error('Error:', error));
});
