#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr


# In[2]:


def formatar_df(dataframe):

    # Formatar coluna de data
    dataframe["Data"] = dataframe["Data"].astype(str)

    # Substituir formatos de data por barras
    substituicoes = [". de ", " de ", ".", " - ", "-", " "]
    substituicoes_para = ["/", "/", "/", "/", "/", ""]

    for orig, para in zip(substituicoes, substituicoes_para):
        dataframe["Data"] = dataframe["Data"].str.replace(orig, para)

    # Substituir iniciais de meses por número correspondente
    meses = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
        "June": "06", "July": "07", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12", "jan": "01",
        "fev": "02", "mar": "03", "abr": "04", "mai": "05", "junho": "06",
        "julho": "07", "jun": "06", "jul": "07", "ago": "08", "set": "09",
        "out": "10", "nov": "11", "dez": "12"
    }

    for mes in meses.keys():
        dataframe["Data"] = dataframe["Data"].str.replace(mes, meses[mes])

    # Transformar a coluna de data em datetime
    formatos_data = ["%Y/%m", "%d/%m/%Y", "%Y/%m/%d"]
    for formato in formatos_data:
        try:
            dataframe["Data"] = pd.to_datetime(dataframe["Data"], format=formato)
            break
        except ValueError:
            continue

    # Definindo linha do tempo
    #dataframe = dataframe[(dataframe["Data"] >= "1995-01-01") & (dataframe["Data"] <= "2024-01-01")]

    dataframe = dataframe.dropna()
    #dataframe.reset_index(drop=True, inplace=True)

    #dataframe.set_index("Data", inplace=True)
    #dataframe.sort_values(by="Data", ascending=True, inplace=True)
    #dataframe = dataframe.resample("MS").first()

    return dataframe


# **Limpeza de dados: PIB do Brasil**

# In[3]:


pib_br = pd.read_csv("PIB 1995-2024.csv", sep=",")
pib_br = pd.DataFrame(pib_br)
pib_br.columns.values[1] = 'PIB Brasil'
pib_br.columns.values[0] = 'Data'
pib_br = formatar_df(pib_br)
pib_br


# **Limpeza de dados: PIB dos EUA**

# In[4]:


pib_usa = pd.read_csv("GDP 1992-2024.csv", sep=",")
pib_usa = pd.DataFrame(pib_usa)
pib_usa = pib_usa.rename(columns={"Unnamed: 0": "Data"})
pib_usa = pib_usa.rename(columns={"Monthly Nominal GDP Index": "PIB EUA"})
pib_usa = pib_usa[["Data", "PIB EUA"]]
pib_usa = formatar_df(pib_usa)
pib_usa


# **Limpeza de dados: IBOV**

# In[5]:


ibov = pd.read_csv("BVSP 1993-2024.csv", sep=",")
ibov = pd.DataFrame(ibov)
ibov = ibov.rename(columns={"Date": "Data"})
ibov = ibov.rename(columns={"Close": "Fechamento IBOV"})
ibov = ibov[["Data", "Fechamento IBOV"]]
ibov = formatar_df(ibov)
ibov


# **Limpeza de dados: S&P500**

# In[6]:


sp500 = pd.read_csv("SP500 1993-2024.csv", sep=",")
sp500 = sp500.rename(columns={"Fechamento*": "Fechamento S&P500"})
sp500 = sp500[["Data", "Fechamento S&P500"]]
sp500 = formatar_df(sp500)
sp500["Fechamento S&P500"] = sp500["Fechamento S&P500"].str.replace(".", "").str.replace(",", ".")
sp500


# In[7]:


dados = pd.merge(pib_usa, pib_br, on="Data")
dados = pd.merge(dados, ibov, on="Data")
dados = pd.merge(dados, sp500, on="Data")
dados = dados.apply(pd.to_numeric, errors="coerce")
dados.describe()


# **Funções para plotagem**

# In[8]:


def plot_regressao(x, y, xlabel, ylabel, title):
    plt.figure(figsize=(10, 6))
    sns.regplot(x=x, y=y, data=dados, ci=None)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def plot_linha_tempo(cols, labels, title):
    plt.figure(figsize=(14, 7))
    for col, label in zip(cols, labels):
        plt.plot(dados.index, dados[col], label=label)
    plt.xlabel("Ano")
    plt.ylabel("Valor")
    plt.title(title)
    plt.legend()
    plt.show()

def correlacao(coluna1, coluna2):
    correlacao, _ = pearsonr(dados[coluna1], dados[coluna2])
    print(f"\nCorrelação: {correlacao}")


# In[9]:


plot_regressao("PIB Brasil", "Fechamento IBOV", "PIB Brasil", "Ibovespa", "Correlação entre PIB Brasil e Ibovespa")
correlacao("PIB Brasil", "Fechamento IBOV")


# In[10]:


plot_regressao("PIB EUA", "Fechamento S&P500", "PIB EUA", "S&P500", "Correlação entre PIB EUA e S&P500")
correlacao("PIB EUA", "Fechamento S&P500")


# In[11]:


plot_linha_tempo(["PIB Brasil", "Fechamento IBOV"], ["PIB Brasil", "Ibovespa"], "PIB Brasil e Ibovespa ao Longo do Tempo")


# In[12]:


plot_linha_tempo(["PIB EUA", "Fechamento S&P500"], ["PIB EUA", "S&P500"], "PIB EUA e S&P500 ao Longo do Tempo (Mensal)")

