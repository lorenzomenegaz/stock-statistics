import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

acao = input("Escolha uma ação para ser analisada: ").upper()

acao = acao + ".SA"

ativos = [acao, "^BVSP"]

dados_completos = yf.download(ativos, "2015-01-01", datetime.now())

cotacoes_ajustadas = dados_completos['Adj Close']

retornos = cotacoes_ajustadas.pct_change().dropna()

retornos['ano'] = retornos.index.year

#retorno acum por ano

retornos[f'{acao}'] = 1 + retornos[f'{acao}'] 
retornos['^BVSP'] = 1 + retornos['^BVSP']

retornos[f'retorno_YTD_{acao}'] = retornos.groupby('ano')[f'{acao}'].cumprod() - 1 
retornos[f'retorno_YTD_ibov'] = retornos.groupby('ano')['^BVSP'].cumprod() - 1 

retorno_por_ano = retornos.groupby('ano').tail(1)[[f'retorno_YTD_{acao}', 'retorno_YTD_ibov']]

print(f"Retorno ano a ano \n{retorno_por_ano*100}\n")

#Estat descritivas da empresa

retornos = cotacoes_ajustadas[f'{acao}'].pct_change().dropna()

retornos = retornos.to_frame()

retornos['ano'] = retornos.index.year

def estatisticas(agrupamento):
    
    return {'min': agrupamento.min() * 100, 'max': agrupamento.max() * 100, 
            'media': agrupamento.mean() * 100, 'vol': agrupamento.std() * np.sqrt(252)}

descritivas = retornos.groupby('ano')[f'{acao}'].apply(estatisticas)

print(f"Estatísticas descritivas: \n{descritivas}\n")

#maxDD

cotacoes_empresa = cotacoes_ajustadas[f'{acao}']

cotacoes_empresa = cotacoes_empresa.to_frame()

cotacoes_empresa['ano'] = cotacoes_empresa.index.year

cotacoes_empresa['maxima_do_ano'] = cotacoes_empresa.groupby('ano')[f'{acao}'].cummax()
cotacoes_empresa['quedas'] = cotacoes_empresa[f'{acao}']/cotacoes_empresa['maxima_do_ano'] - 1

print(f"Max DD: \n{cotacoes_empresa.groupby('ano')['quedas'].min()}\n")

#grafico de cor contra o ibov

retornos = cotacoes_ajustadas.pct_change().dropna()

retornos[f'{acao}'].rolling(252).corr(retornos['^BVSP']).dropna().plot()

#volume medio anual

volume_acoes = dados_completos['Volume'][f'{acao}']
cotacao =  dados_completos['Close'][f'{acao}']

volume_financeiro = volume_acoes * cotacao

volume_financeiro = volume_financeiro.to_frame()

volume_financeiro['ano'] = volume_financeiro.index.year

volume_medio = volume_financeiro.groupby('ano').mean()

volume_medio = volume_medio.astype(int)

print(f"Volume negociado: \n{volume_medio}\n")
