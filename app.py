from flask import Flask, request, render_template
from scipy.stats import binom

def calcular_ITM(n, Pa, N):
    return n + (1 - Pa) * (N - n)

def calcular_riscos_e_custos(N, custo_unitario_inspecao, despesa_lote_reprovado, NQA, n, a, taxa_defeituosos, dias_uteis_mes, PTDL):
    # Cálculo dos riscos
    risco_fornecedor = 1 - binom.cdf(a, n, NQA / 100)
    risco_consumidor = binom.cdf(a, n, PTDL / 100)
    # Cálculo da probabilidade de aceitação considerando a taxa de defeitos atual
    Pa = binom.cdf(a, n, taxa_defeituosos / 100)
    # Cálculo da Inspeção Total Média (ITM) considerando a taxa de defeitos atual
    ITM = calcular_ITM(n, Pa, N)
    # Cálculo dos custos de inspeção
    custo_inspecao = dias_uteis_mes * ITM * custo_unitario_inspecao
    custo_lotes_rejeitados = dias_uteis_mes * (1 - Pa) * despesa_lote_reprovado
    # Determinação de aceitação ou rejeição do lote
    lote_aceito = Pa > (1 - PTDL / 100)
    # Cálculo do custo total considerando lotes reprovados
    custo_total = custo_inspecao + custo_lotes_rejeitados
    # Resultados
    return risco_fornecedor, risco_consumidor, custo_inspecao, custo_total, ITM, custo_lotes_rejeitados, lote_aceito

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lote = int(request.form['lote'])
        dias = int(request.form['dias'])
        custo_unit_insp = float(request.form['custo_insp'])
        custo_lote = float(request.form['custo_lote'])
        nqa = float(request.form['nqa'])
        ptdl = float(request.form['ptdl'])
        #risco_fornecedor_max = float(request.form['riscos-fornecedor'])
        tamanho_amostra = int(request.form['amostra'])
        aceitacao_maxima = float(request.form['a'])
        taxa_defeituosos_forn = float(request.form['taxa_defeituosos'])

        risco_fornecedor, risco_consumidor, custo_inspecao, custo_total, ITM, custo_lote, lote_aceito = calcular_riscos_e_custos(
        lote, custo_unit_insp, custo_lote, nqa, tamanho_amostra, aceitacao_maxima, taxa_defeituosos_forn, dias, ptdl)

        
        if lote_aceito == True:
            resultado = {
                    'Custo de Inspeção': custo_inspecao,
                    'Custo de Despesas': custo_lote,
                    'Custo Total': custo_total,
                    'Inspeção Total Média (ITM)': ITM,
                    'risco_fornecedor': risco_fornecedor,
                    'risco_consumidor': risco_consumidor,
                    'Lote aceito': 'Sim'
                    }
        else:
            resultado = {
                    'Custo de Inspeção': custo_inspecao,
                    'Custo de Despesas': custo_lote,
                    'Custo Total': custo_total,
                    'Inspeção Total Média (ITM)': ITM,
                    'risco_fornecedor': risco_fornecedor,
                    'risco_consumidor': risco_consumidor,
                    'Lote aceito': 'Não'
                    }
        return render_template('index.html', resultado=resultado)
    
    return render_template('index.html', resultado=None)

if __name__ == '__main__':
    app.run(debug=True)
