import pandas as pd


def carregar_dados():

    print("\n --- FASE DE EXTRAÇÃO--- \n")

    df = pd.read_csv("data/raw/adult.csv") #lê o arquivo CSV e cria uma Dataframe

    return df
    


def transformar_dados(df):
    pass


def gerar_relatorios(df):
    pass


def salvar_dados(df):
    pass


def main():
    df = carregar_dados()
    print("\nDataFrame carregado!\n")
    


if __name__ == "__main__":
    main()