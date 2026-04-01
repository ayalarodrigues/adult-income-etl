import pandas as pd


def carregar_dados():

    '''Etapa de extração.
    Lê o arquivi principal da base adult e retorna um DataFrame'''

    print("\n --- FASE DE EXTRAÇÃO--- \n")

    df = pd.read_csv("data/raw/adult.csv") #lê o arquivo CSV e cria uma Dataframe

    return df
    

def criar_tabela_regioes():
    """
    Aqui, usei o Gemini para gerar esse dicionário com o nome dos países.
    Cria um dicionário com duas listas: uma com os países e outra com a região de cada país.
    """

    registros = [
        # América do Norte
        ("United-States", "america_norte"),
        ("Canada", "america_norte"),
        ("Mexico", "america_norte"),

        # América Central e Caribe
        ("Puerto-Rico", "america_central_caribe"),
        ("Cuba", "america_central_caribe"),
        ("Dominican-Republic", "america_central_caribe"),
        ("Jamaica", "america_central_caribe"),
        ("Haiti", "america_central_caribe"),
        ("Honduras", "america_central_caribe"),
        ("Guatemala", "america_central_caribe"),
        ("Nicaragua", "america_central_caribe"),
        ("El-Salvador", "america_central_caribe"),
        ("Trinadad&Tobago", "america_central_caribe"),

        # América do Sul
        ("Columbia", "america_sul"),
        ("Ecuador", "america_sul"),
        ("Peru", "america_sul"),

        # Europa
        ("England", "europa"),
        ("France", "europa"),
        ("Germany", "europa"),
        ("Greece", "europa"),
        ("Holand-Netherlands", "europa"),
        ("Hungary", "europa"),
        ("Ireland", "europa"),
        ("Italy", "europa"),
        ("Poland", "europa"),
        ("Portugal", "europa"),
        ("Scotland", "europa"),
        ("Yugoslavia", "europa"),

        # Ásia
        ("Cambodia", "asia"),
        ("China", "asia"),
        ("Hong", "asia"),
        ("India", "asia"),
        ("Iran", "asia"),
        ("Japan", "asia"),
        ("Laos", "asia"),
        ("Philippines", "asia"),
        ("Taiwan", "asia"),
        ("Thailand", "asia"),
        ("Vietnam", "asia"),
        ("South", "asia"),

        # Grupo específico para territórios dos EUA
        ("Outlying-US(Guam-USVI-etc)", "territorios_eua"),
    ]

    tabela_regioes = pd.DataFrame(
        registros,
        columns=["native_country", "world_region"]
    )

    print("\nTabela auxiliar de regiões criada com sucesso.")
    print(tabela_regioes.head(10))
    print("\nQuantidade de países mapeados:", len(tabela_regioes))

    return tabela_regioes


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

    # ---------------------------------------------------------------------- #

    # Nova variável 3: Classificação de carga horária semanal#

    '''A ideia aqui é transformar uma variável quantitativa em faixas de valores para futuras interpretações'''

    #recebe um número e devolve uma categoria textual
    def classificar_carga_horaria(horas):
        if horas < 35:
            return "baixa"
        elif horas < 45:
            return "normal"
        else:
            return "alta"
    df["weekly_workload"] = df["hours_per_week"].apply(classificar_carga_horaria)

    print("\nColuna weekly_workload criada!\n")
    print(df[["hours_per_week", "weekly_workload"]].head(10))

    print("\nDistribuição da coluna weekly_workload:")
    print(df["weekly_workload"].value_counts())

    # ---------------------------------------------------------------------- #

    # Nova variável 4: Agrupamento educacional#
    
    '''A coluna 'education' possui muitas categorias.
    Aqui elas são agrupadas em blocos de classificação para facilitar futuras análises'''

    def agrupar_escolaridade(educacao):
        if educacao in [
            "preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th", "11th", "12th"
        ]:
            return "basico"
        elif educacao in ["HS-grad", "Some-college"]:
            return "medio"
        elif educacao in ["Assoc-acdm", "Assoc-voc", "Bachelors"]:
            return "superior"
        else:
            return "pos-graduacao"
        

    df["education_group"] = df["education"].apply(agrupar_escolaridade)    
    
    print("\nColuna education_group criada!")
    print(df[["education", "education_group"]].head(15))

    print("\nDistribuição da coluna education_group:")
    print(df["education_group"].value_counts())

    tabela_regioes = criar_tabela_regioes()

    #faz a junção da base com a tabela auxiliar
    df = df.merge(tabela_regioes, on = "native_country", how="left") #left mantém todas as linhas da base e apenas acrescenta a região quando houver uma correspondência
    #a chave de junção é a coluna de país (on="native_country")
    print("\nMerge com tabela de regiões realizado.")
    print(df[["native_country", "world_region"]].head(15))

    print("\nQuantidade de nulos na coluna world_region após o merge:")
    print(df["world_region"].isna().sum()) #conta quantos registros dicaram sem região depois do merge

    #Caso alguma categoria esteja sem região, preenche com 'regiao_desconhecida'
    df["world_region"] = df["world_region"].fillna("regiao_desconhecida")

    print("\nDistribuição da coluna world_region:")
    print(df["world_region"].value_counts())

    return df


def gerar_relatorios(df):

    '''Etapa de análise:
    Gera resumos agregados com groupby()
    para apoio do relatório e das exportações'''

    print("\n Etapa de Análise com GroupBy\n")

    #dicionário vazio
    relatorios = {}

    # --------------- Análise 1: Resumo por sexo ------------------ #

    renda_por_sexo = (
        df.groupby("sex").agg( #agrupa os dados por sexo e aplica várias métricas d euma vez com o agg
            total_registros = ("income_binary", "count"), #conta quantos registros existem por sexo
            idade_media = ("age", "mean"), #calcula a média da idade por sexo
            horas_media_semanais = ("hours_per_week", "mean"), #calcula a média das horas semanais
            proporcao_renda_alta = ("income_binary", "mean") #calcula a média da variável binária, que seria a proporção de pessoas com renda alta
        ).reset_index()
    )

    #converte proporção em percentual
    renda_por_sexo["percentual_renda_alta"] = renda_por_sexo["proporcao_renda_alta"] * 100

    print("\nAnálise 1 - Renda por sexo\n")
    print(renda_por_sexo)

    relatorios["renda_por_sexo"] = renda_por_sexo


    # --------------- Análise 2: Resumo por Agrupamento Educacional ------------------ #

    renda_por_escolaridade = (df.groupby("education_group").agg( #agrupa pelos blocos educacionais criados(basico, medio, superior, pos_graduacao)
        total_registros = ("income_binary", "count"),
        renda_alta_percentual = ("income_binary", "mean"), #uso da média da variável binária como porporção de renda alta
        idade_media = ("age", "mean"),
        mediana_horas_semanais = ("hours_per_week", "median"), #coloca uma mediana
        media_anos_estudo=("education_num", "mean"), #aproveita a coluna numérica de educação para dar um resumo adicional 
    ).reset_index())

    renda_por_escolaridade["renda_alta_percentual"] = (
        renda_por_escolaridade["renda_alta_percentual"]* 100
    )

    print("\nAnálise 2 - Renda por agrupamento educacional:")
    print(renda_por_escolaridade)

    relatorios["renda_por_escolaridade"] = renda_por_escolaridade

    # --------------- Análise 3: Resumo por Faixa Etária ------------------ #

    renda_por_faixa_etaria = (df.groupby("age_group").agg(
        total_registros = ("income_binary", "count"),
        renda_alta_percentual = ("income_binary", "mean"),
        idade_media = ("age", "mean"),
        idade_mediana = ("age", "median"),
        horas_media_semanais = ("hours_per_week", "mean"),
        escolaridade_media = ("education_num", "mean"),
    ).reset_index())


    renda_por_faixa_etaria["renda_alta_percentual"] = (
        renda_por_faixa_etaria["renda_alta_percentual"] * 100
    )

    print("\nAnálise 3 - Renda por faixa etária:")
    print(renda_por_faixa_etaria)

    relatorios["renda_por_faixa_etaria"] = renda_por_faixa_etaria

    # --------------- Análise 4: Resumo por Carga horária semanal ------------------ #

    renda_por_carga_horaria = (df.groupby("weekly_workload").agg(
        total_registros = ("income_binary", "count"),
        renda_alta_percentual = ("income_binary", "mean"),
        horas_media_semanais = ("hours_per_week", "mean"),
        idade_media=("age", "mean"),
        escolaridade_media = ("education_num", "mean"),
    ).reset_index())

    renda_por_carga_horaria["renda_alta_percentual"] = (
        renda_por_carga_horaria["renda_alta_percentual"] * 100
    )

    print("\nAnálise 4 - Renda por carga horária semanal:")
    print(renda_por_carga_horaria)

    relatorios["renda_por_carga_horaria"] = renda_por_carga_horaria

    # --------- Análise 5: Resumo da Região Geográfica -------------

    renda_por_regiao = (
        df.groupby("world_region").agg(
            total_registros = ("income_binary", "count"),
            renda_alta_percentual = ("income_binary", "mean"),
            idade_media =("age", "mean"),
            horas_media_semanais = ("hours_per_week", "mean"),
        ).reset_index()
    )

    renda_por_regiao["renda_alta_percentual"] = (
        renda_por_regiao["renda_alta_percentual"] * 100
    )

    print("\nAnálise 5 - Renda por Região Geográfica:\n")
    print(renda_por_regiao)

    relatorios["renda_por_regiao"] = renda_por_regiao


    print("\n --- ETAPA DE ORGANIZAÇÃO COM PIVOT TABLE ---\n")

    # --------------------------------------------------- #

    # PIVOT 1: Percentual de Renda alta por escolaridade  #


    pivot_renda_sexo_escolaridade = pd.pivot_table(
        df,
        index = "education_group", #as linahs da tabela serão os grupos educacionais
        columns="sex", #as colunas da tabela serão o sexo
        values="income_binary", #o valor analisado será a coluna binária de renda
        aggfunc="mean", #agregação será a média
        fill_value=0, #se falta algo, preenche com zero
    )

    pivot_renda_sexo_escolaridade = pivot_renda_sexo_escolaridade * 100

    print("\nPivot 1 - Percentual de renda alta por escolaridade e sexo:\n")
    print(pivot_renda_sexo_escolaridade)

    # --------------------------------------------------- #

    # PIVOT 2: Média de horas semanais por regiao e faixa etária  #


    pivot_horas_regiao_idade = pd.pivot_table(
        df,
        index="world_region",
        columns="age_group",
        values="hours_per_week",
        aggfunc="mean",
        fill_value=0,
    )

    print("\nPivot 2 - Média de horas semanais por região e faixa etária:\n")
    print(pivot_horas_regiao_idade)






    return relatorios
    


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

    relatorios = gerar_relatorios(df)
    print("\nRelatórios gerados:")
    print(relatorios.keys())


    #df = transformar_dados(df)
          

if __name__ == "__main__":
    main()



#tempo médio de trabalho por status marital
#tempo de trabalho por gênero - ração
#salaŕio por tempo d etrabalho

#binario com 0 e 1 para renda
