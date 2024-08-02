from flask import Flask, request, render_template
from scipy.stats import binom

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lote = int(request.form['lote'])
        nqa = float(request.form['nqa'])
        ptdl = float(request.form['ptdl'])
        risco_fornecedor_max = float(request.form['riscos-fornecedor'])
        risco_consumidor_max = float(request.form['riscos-consumidor'])

        plano_encontrado = False
        tamanho_amostra = 0
        aceitacao_maxima = 0

        for n in range(1, lote + 1):
            for c in range(n + 1):
                risco_fornecedor = 1 - binom.cdf(c, n, nqa)
                risco_consumidor = binom.cdf(c, n, ptdl)

                if risco_fornecedor <= risco_fornecedor_max and risco_consumidor <= risco_consumidor_max:
                    plano_encontrado = True
                    tamanho_amostra = n
                    aceitacao_maxima = c
                    break
            if plano_encontrado:
                break

        if plano_encontrado:
            resultado = {
                'tamanho_amostra': tamanho_amostra,
                'aceitacao_maxima': aceitacao_maxima,
                'risco_fornecedor': f"{risco_fornecedor:.3f}",
                'risco_consumidor': f"{risco_consumidor:.3f}"
            }
        else:
            resultado = None
        
        return render_template('index.html', resultado=resultado)
    
    return render_template('index.html', resultado=None)

if __name__ == '__main__':
    app.run(debug=True)
