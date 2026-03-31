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
    for coluna in colunas_categoria: #percorre cada coluna categórica
        df[coluna] = df[coluna].str.strip()
    
    print("\nEspaços extras foram removidos das colunas categóricas!\n")
    print("\nAmostra das colunas textuais após strip:")
    print(df[colunas_categoria].head())

    #Mo
    print("\Categorias únicas de workclass:")
    print(df["workclass"].dropna().unique()) #dropna remove nulos da visualização / unique mostra valores únicos da coluna

    print("\nCategorias únicas de occupation:")
    print(df["occupation"].dropna().unique())

    print("\Categorias únicas de native_country:")
    print(df["native_country"].dropna().unique()[:10])

    '''
    #Aplicação da moda para colunas textuais(categóricas) com dados nulos
    print("\n --- TRATAMENTO DE DADOS AUSENTES COM MODA --- \n")
    print("Moda workclass:")
    print(df["workclass"].mode()) #calcula a moda da coluna, ou seja, o valor que aparece com maior frequência

    print("\nModa occupation:")
    print(df["occupation"].mode())

    print("\nModa native_country:")
    print(df["native_country"].mode())
    '''
    #cálculo de modas
    moda_workclass = df["workclass"].mode()[0] #retorna uma série com a moda e pegamos o primeiro valor com [0]
    moda_occupation = df["occupation"].mode()[0]
    moda_native_country = df["native_country"].mode()[0]

    print("\nModa workclass:", moda_workclass)
    print("\nModa occupation:", moda_occupation)
    print("\nModa native_country:", moda_native_country)

    #Preenchimento de dados ausentes com a moda da coluna
    df["workclass"] = df["workclass"].fillna(moda_workclass)
    df["occupation"] = df["occupation"].fillna(moda_occupation)
    df["native_country"] = df["native_country"].fillna(moda_native_country)

    print("\nQuantidade de nulo por coluna após tratamento com moda:")
    print(df.isna().sum())

    #cria uma lista de colunas que devem ser numéricas
    colunas_numericas = [
        "age",
        "fnlwgt",
        "education_num",
        "capital_gain",
        "capital_loss",
        "hours_per_week",
    ]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce") #coerce é usado pq se aparecer algum valor inválido, ele vira um nulo em vez de gerar um erro
    
    print("\nTipos de dados após ajuste:")
    print(df.dtypes)

    # ---------------------------------------------------------------------- #

    # Nova variável 1: Indicador de renda #

    '''Converte a variável categórica 'income' em uma variável binária:
    0 para renda menor ou igual a 50K
    1 para renda maior que 50K
    Essa transformação visa facilitar análises futuras'''

    #o map pega cada valor da coluna income e procura esse valor no dicionário
    #se encontrar <=50K, troca por 0
    df["income_binary"] = df["income"].map({
        "<=50K": 0,
        ">50K": 1
    })
    
    print("\nColuna income_binary criada!\n")
    print(df[["income", "income_binary"]].head(10))

    print("\nDistribuição de income_binary:")
    print(df["income_binary"].value_counts(dropna=False)) #value_counts conta quantas vezes cada valor aparece
    #dropna=False porque, caso o mapeamento tenha algum problema, isso mostra possíveis NaN

    # ---------------------------------------------------------------------- #

    # Nova variável 2: Faixa etária com apply #

    '''A coluna 'age' é numérica. 
    Aqui ela é convertida em uma categoria para análises agregadas'''

    #função que define os critérios de classificação das idades
    def classificar_faixa_etaria(idade):
        if idade < 30:
            return "jovem"
        elif idade < 50:
            return "adulto"
        elif idade < 65:
            return "meia-idade"
        else:
            return "idoso"
    
    #apply pega o valor da coluna 'age', chama a função e devolve o resultado em uma nova coluna
    #pega uma idadem verifica em qual faixa ela se encaixa e grava a categoria correspondente em 'age_group'
    df["age_group"] = df["age"].apply(classificar_faixa_etaria)

    print("\nColuna age_group criada com apply!\n")
    print(df[["age", "age_group"]].head(10))

    print("\nDistribuição da coluna age_group:")
    print(df["age_group"].value_counts())

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

    #Atualiza o df com base já transformada
    df = transformar_dados(df)

    print("\nBase após transformação:")
    print(df.head())

    print("Dimensão da base após transformação:")
    print(df.shape)


    #df = transformar_dados(df)
          

if __name__ == "__main__":
    main()