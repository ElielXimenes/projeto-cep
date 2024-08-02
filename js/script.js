function binomCDF(k, n, p) {
    let cdf = 0;
    for (let i = 0; i <= k; i++) {
        cdf += binomPMF(i, n, p);
    }
    return cdf;
}

function binomPMF(k, n, p) {
    function factorial(x) {
        if (x === 0) return 1;
        let f = 1;
        for (let i = 1; i <= x; i++) {
            f *= i;
        }
        return f;
    }
    return (factorial(n) / (factorial(k) * factorial(n - k))) * Math.pow(p, k) * Math.pow(1 - p, n - k);
}

function calcularPlanoAmostral() {
    const lote = parseInt(document.getElementById('lote').value);
    const nqa = parseFloat(document.getElementById('nqa').value);
    const ptdl = parseFloat(document.getElementById('ptdl').value);
    const riscoFornecedorMax = parseFloat(document.getElementById('riscos-fornecedor').value);
    const riscoConsumidorMax = parseFloat(document.getElementById('riscos-consumidor').value);

    let tamanhoAmostra = 0;
    let aceitacaoMaxima = 0;
    let riscoFornecedor = 0;
    let riscoConsumidor = 0;

    let planoEncontrado = false;

    for (tamanhoAmostra = 1; tamanhoAmostra <= lote; tamanhoAmostra++) {
        for (aceitacaoMaxima = 0; aceitacaoMaxima <= tamanhoAmostra; aceitacaoMaxima++) {
            riscoFornecedor = 1 - binomCDF(aceitacaoMaxima, tamanhoAmostra, nqa);
            riscoConsumidor = binomCDF(aceitacaoMaxima, tamanhoAmostra, ptdl);

            if (riscoFornecedor <= riscoFornecedorMax && riscoConsumidor <= riscoConsumidorMax) {
                planoEncontrado = true;
                break;
            }
        }
        if (planoEncontrado) break;
    }

    const resultElement = document.getElementById('value');
    const descriptionElement = document.getElementById('descricao');
    const infoSection = document.getElementById('infos');

    if (planoEncontrado) {
        resultElement.innerText = `Tamanho da amostra: ${tamanhoAmostra}\nÍndice de aceitação máxima: ${aceitacaoMaxima}\nRisco do fornecedor: ${riscoFornecedor.toFixed(3)}\nRisco do consumidor: ${riscoConsumidor.toFixed(3)}`;
        descriptionElement.innerText = '';
    } else {
        resultElement.innerText = 'Nenhum plano amostral encontrado.';
        descriptionElement.innerText = 'Verifique os parâmetros e tente novamente.';
    }

    infoSection.classList.remove('hidden');
}


    const resultElement = document.getElementById('value');
    const descriptionElement = document.getElementById('descricao');
    const infoSection = document.getElementById('infos');

    if (planoEncontrado) {
        resultElement.innerText = `Tamanho da amostra: ${tamanhoAmostra}\nÍndice de aceitação máxima: ${aceitacaoMaxima}\nRisco do fornecedor: ${riscoFornecedor.toFixed(3)}\nRisco do consumidor: ${riscoConsumidor.toFixed(3)}`;
        descriptionElement.innerText = '';
    } else {
        resultElement.innerText = 'Nenhum plano amostral encontrado.';
        descriptionElement.innerText = 'Verifique os parâmetros e tente novamente.';
    }

    infoSection.classList.remove('hidden');
