# Importar pacotes necessários
import numpy as np #Biblioteca de cálculos númericos do Python
import pandas as pd #Biblioteca de analise de dados
import matplotlib.pyplot as plt #Biblioteca de analise de dados e plotagem de gráficos
import seaborn as sns #Biblioteca auxiliar ou complementar de analise de dados e plotagem de gráficos
import tkinter as tk #Biblioteca de GUi padrão do python
from tkinter import ttk #Addon opcional da TKInter
from tkinter import messagebox #Importa o modulo de caixas de aviso
import sys #Biblioteca de interface de comandos com o sistema operacional

try:
    df = pd.read_csv('master.csv') # Lê o banco de dados
except:
    tk.messagebox.showerror(title = 'Arquivo "master.csv" não encontrado', message = 'Arquivo do banco de dados não encontrado, verifique se ele está localizado na raiz do arquivo executável.')
    sair()

# Funções
paisEscolhido = []
def verificaSelecao(): # Seleciona o país para ser gerado os gráficos em relação a ele
    paisEscolhido.append(str(escolhePais.get()))
    janelaPais.quit() # Saí do loop da janela
    confirma.config(state = 'disabled') # Desabilita alteração de dados nos botões
    escolhePais.config(state = 'disabled')
    info.config(state = 'normal')
    textoPais.config(text = 'País selecionado,\ngráficos em exibição')

def sair(): # Função relativa ao botão Sair (sair) e evento de fechar janela ('WM_DELETE_WINDOW')
    sys.exit(0)

def informacoes(): # Função relativa ao botão Informações (info)
    janelaDados = tk.Tk()
    try:
        janelaDados.iconbitmap('icon.ico')
    except:
        tk.messagebox.showwarning(title = 'Arquivo "icon.ico" não encontrado', message = 'Arquivo de ícone não encontrado, verifique se ele está localizado na raiz do arquivo executável.')
    janelaDados.title("Informações - Debug")
    janelaDados.geometry('1120x480')
    
    # Formatação da caixa de texto
    f = tk.Frame(janelaDados)
    f.place(x=10, y=10)
    scrollbar = tk.Scrollbar(f)
    textoInfo = tk.Text(f, bg = '#FFFFFF', width=120, font = 'Consolas',  yscrollcommand = scrollbar.set)
    textoInfo.tag_configure("center", justify='center')
    scrollbar.config(command = textoInfo.yview)

    # Calcular informações sobre o dataframe
    textoInfo.insert('insert', str('Formato do DataFrame: ' + str(df.shape) + '\n'), 'center') # Ver o formato do DataFrame
    textoInfo.insert('insert', str( df.head() ) ) # Ver as 5 primeiras entradas dos dataset
    
    # Ver o formato do DataFrame Escolhido
    textoInfo.insert('insert', str("\nFormato do DataFrame Escolhido: " + str(paisEscolhido[-1]) + str(df_escolhido.shape) + '\n' ), 'center' ) 
    textoInfo.insert('insert', str( df_escolhido.head() ) ) # Ver as 5 primeiras entradas dos dataset escolhido
    
    # Valores ausentes nos dados mundiais
    textoInfo.insert('insert', str('\n--> Mundial:' + str(df.isnull().sum()) + "\n" + "--." * 10 + "\n") )

    # Valores ausentes nos dados do pais escolhido
    textoInfo.insert('insert', str('\n--> ' + str(paisEscolhido[-1]) + ':' + str(df_escolhido.isnull().sum()) + "\n" + "--." * 10 + "\n") )
    
    # Ver as 5 primeiras entradas da pivot table
    textoInfo.insert('insert', str(table.head()))

    textoInfo.config(state = 'disabled')
    scrollbar.pack(side='right', fill='y')
    textoInfo.pack()

def separarPaises(): # Separa os nomes dos países para aparecer no drop-down menu, ou command box
    col_list = ["country"]
    try:
        df = pd.read_csv("master.csv", usecols=col_list) # Separa a coluna 'country' para poder manipulá-la
    except:
        tk.messagebox.showerror(title = 'Arquivo "master.csv" não encontrado', message = 'Arquivo do banco de dados não encontrado, verifique se ele está localizado na raiz do arquivo executável.')
        sair()
    arr = df.to_numpy()
    paises = []
    flattened = []
    for pais in arr:
        if pais not in paises:
            paises.append(pais) # Adiciona os países em uma lista
    for sublist in paises:
        for val in sublist:
            flattened.append(val)  # Transforma a lista de listas dos países em uma única lista
    return flattened

def retornaAnosFaltantes(dframe, paisSelecionado):# Como alguns países não possuem dados de alguns anos, esses anos faltantes são anotados em uma lista
    anosFaltantes = []
    anosPresentes = []
    df = dframe
    filtro = dframe['country'].str.contains(paisSelecionado) # Filtra o dataframe para utilizar somente o país selecionado pelo usuário
    separaPais = df[filtro] 
    for i in separaPais['year']:
        for j in range(1985, 2017):
            if i == j:
                if i not in anosPresentes: # Cria uma lista com os anos em que há dados do país selecionado
                    anosPresentes.append(i)
    for i in range(1985, 2017):
        if i not in anosPresentes:
            anosFaltantes.append(i) # Cria uma lista com os anos onde não há dados do país
    return anosFaltantes

def limpaAnosFaltantes(anosFaltantes): # Como alguns países não possuem dados de alguns anos, esses dados são eliminados
    for ano in anosFaltantes:
        suicides_world_mean.drop(ano, inplace=True)

# Janela de seleção de pais#
janelaPais = tk.Tk()
try:
    janelaPais.iconbitmap('icon.ico')
except:
    tk.messagebox.showwarning(title = 'Arquivo "icon.ico" não encontrado', message = 'Arquivo de ícone não encontrado, verifique se ele está localizado na raiz do arquivo executável.')
janelaPais.title('Setembro Amarelo')
janelaPais.geometry('300x250')
janelaPais.protocol('WM_DELETE_WINDOW', sair)
# Widgets
textoPais = tk.Label(master = janelaPais, text = 'Selecione o país a ser analisado:', font = '12') # Texto
textoPais.place(relx=0.5, rely=0.3, anchor='center')
escolhePais = ttk.Combobox(janelaPais, # Lista de países
                           values = separarPaises(),
                           state = 'readonly')
escolhePais.current(15)
escolhePais.place(relx=0.5, rely=0.5, anchor='center')
confirma = ttk.Button(janelaPais, text = 'Confirma', command = verificaSelecao, state = 'active')# B Botãão de confirmação
confirma.place(relx=0.5, rely=0.6, anchor='center')
info = ttk.Button(janelaPais, text = 'Informações', command = informacoes, state = 'disabled')# B Botãão de saída
info.place(relx=0.5, rely=0.7, anchor='center')
sair = ttk.Button(janelaPais, text = 'Sair', command = sair)# Botão de saída
sair.place(relx=0.5, rely=0.9, anchor='center')
janelaPais.mainloop() #Mantém janela aberta

## Extrair apenas os dados relativos ao Pais Escolhido
df_escolhido = df[df.country == str(paisEscolhido[-1])].copy()

##Gráfico de linhas
# Calcular a media mundial e do Brasil em suicidios
years = df_escolhido.year.unique()    # Pegar os anos para o eixo x
suicides_brasil_mean = df_escolhido.groupby('year')['suicides/100k pop'].mean()
suicides_world_mean = df.groupby('year')['suicides/100k pop'].mean()


limpaAnosFaltantes(retornaAnosFaltantes(df, paisEscolhido[-1]))

# Plotar lineplot comparativo entre o Pais Escolhido e Mundo
plt.figure(num = 'Gráfico de linhas', figsize=(6,5), dpi=100)
sns.lineplot(x=years, y=suicides_brasil_mean, label=str(paisEscolhido[-1]))
sns.lineplot(x=years, y=suicides_world_mean, label='Mundo')
plt.legend(title="Taxa de suicídio")
plt.plot()

##Gráfico das faxas etárias 
# Criar uma tabela dinâmica
table = pd.pivot_table(df_escolhido, values='suicides_no', index=['year'], columns=['age'])
# Reordenar as tableas para deixar em ordem crescente
column_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years']
table = table.reindex(column_order, axis=1)
# Plotar a pivot table das faixas etárias
table.plot.bar(stacked=True, figsize=(16,8))
plt.legend(title="Idade")
plt.plot()

##Gráfico de Pizza:
# Extrair valores entre homens e mulheres
homens_mulheres = df_escolhido.groupby('sex').suicides_no.sum() / df_escolhido.groupby('sex').suicides_no.sum().sum()
# Plotar o gráfico
plt.figure(num = 'Gráfico de Pizza')
plt.pie(homens_mulheres, labels=['Mulheres', 'Homens'], autopct='%1.2f%%', shadow=True)
plt.plot()

plt.show() # Exibir os gráficos plotados


try:
    janelaDados.mainloop()
except:
    pass