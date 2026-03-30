import pandas as pd


def carregar_dados():

    '''Etapa de extração.
    Lê o arquivi principal da base adult e retorna um DataFrame'''

    print("\n --- FASE DE EXTRAÇÃO--- \n")

    df = pd.read_csv("data/raw/adult.csv") #lê o arquivo CSV e cria uma Dataframe

    return df
    


def transformar_dados(df):
    '''Etapa inicial da transformação:
    ajuste de nomes de colunas para um padrão'''

    print("\n --- FASE DE TRANSFORMAÇÃO ---\n")

    #renomeia colunas do dataframe ao passar um dicionário
    df = df.rename(
        columns ={
            "educational-num": "education_num",
            "marital-status": "marital_status",
            "capital-gain": "capital_gain",
            "capital-loss": "capital_loss",
            "hours-per-week": "hours_per_week",
            "native-country": "native_country",
            "gender": "sex"
        }
    )

    print("\nColunas renomeadas:\n")
    print(df.columns.tolist())

    #Substitui o símbolo ? por um valor nulo real
    df = df.replace("?", pd.NA) #procura o valor '?' no df e troca por um valor ausente/nulo(pd.NA)
    print("\nA Substituição do símbolo '?' por um nulo foi realizada!")

    #COntar nulos por coluna
    print("\nQuantidade de nulos por coluna:")
    print(df.isna().sum()) #verifica, célula por célula, se o valor é nulo. Retorna True para ausente e False para preenchido. sum() soma os True.

    #seleciona colunas categóricas/textuais
    colunas_categoria = df.select_dtypes(include=["object"]).columns.tolist() #object seleciona colunas de texto
    
    print("\nColunas categóricas para limpeza de texto:")

    #Remove espaços extras do início e fim
    for coluna in colunas_categoria:
        df[coluna] = df[coluna].str.strip()
    
    print("\nEspaços extras foram removidos das colunas categóricas!\n")
    print("\nAmostra das colunas textuais após strip:")
    print(df[colunas_categoria].head())

    
    return df


def gerar_relatorios(df):
    pass


def salvar_dados(df):
    pass


def main():
    df = carregar_dados()
    print("\nDataFrame carregado!\n")

    #mostra as primeiras 5 linhas
    print("\nPrimeiras 5 linhas:\n")
    print(df.head())

    #mostra os nomes das colunas
    print("\nNomes das colunas:\n")
    print(df.columns.to_list()) #df.columns sozinho retorna um objeto do pandas. O to_list transforma em uma lista simples de py.

    #mostra tipos e quantidade de valores 
    print("\nInformações sobre a base:\n")
    print(df.info())

    #mostra estatísticas das colunas numéricas
    print("\nEstatísticas descritivas:\n")
    print(df.describe())

    #mostra dimensão da base
    print("\nDimensão da base:\n")
    print(df.shape) #mostra a dimensão da base no formato (linhas, colunas)

    print("\n--- IDENTIFICAÇÃO DOS TIPOS DE COLUNAS DA BASE ---\n")

    #seleciona colunas numéricas
    colunas_numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist() #dtypes seleciona colunas com base em um tipo de dado(no caso, pede que sejam inteiros e decimais)
    #seleciona colunas categóricas/textuais
    colunas_categoria = df.select_dtypes(include=["object"]).columns.tolist() #object seleciona colunas de texto

    print("\nColunas numéricas:\n")
    print(colunas_numericas)

    print("\nColunas categóricas:\n")
    print(colunas_categoria)


    df = transformar_dados(df)
          

if __name__ == "__main__":
    main()