from fuzzywuzzy import process
import pandas as pd
from sklearn.preprocessing import StandardScaler,LabelEncoder
import joblib
import yaml
import psycopg2
import const
import boto3
from io import StringIO

# Conexao com banco de dados
def fetch_data_from_db():
    try:
        # Abrir o arquivo de configuração
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        # Acessar as credenciais e dados de configuração
        aws_access_key = config['database_config']['aws_access_key']
        aws_secret_key = config['database_config']['aws_secret_key']
        bucket_name = config['database_config']['bucket_name']
        file_key = config['database_config']['file_key']
        
        # Conectar ao S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name='sa-east-1'  # Ou a região do seu bucket S3
        )

        # Obter o objeto do S3
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)

        # Ler o conteúdo do arquivo CSV para um DataFrame
        df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))

        return df

    except Exception as e:
        print(f"Erro ao conectar com AWS S3: {e}")
        return None

# Funcao para substituir registros nulos
def substitui_nulos(df):
    for coluna in df.columns:
        if df[coluna].dtype == 'object':
            moda = df[coluna].mode()[0]
            df[coluna].fillna(moda, inplace=True)
        else:
            mediana = df[coluna].median()
            df[coluna].fillna(mediana, inplace=True)

# Corrigir erros de digitacao 
def corrigir_erros_digitacao(df, coluna, lista_valida):
    for i, valor in enumerate(df[coluna]):
        valor_str = str(valor) if pd.notnull(valor) else valor

        if valor_str not in lista_valida and pd.notnull(valor_str):
            correcao = process.extractOne(valor_str, lista_valida)[0]
            df.at[i, coluna] = correcao

# Tratar outliers
def tratar_outliers(df, coluna, minimo, maximo):
    mediana = df[(df[coluna] >= minimo) & (df[coluna] <= maximo)][coluna].median()
    df[coluna] = df[coluna].apply(lambda x: mediana if x < minimo or x > maximo else x)
    return df

def save_scalers(df, nome_colunas):
    for nome_coluna in nome_colunas:
        scaler = StandardScaler()
        df[nome_coluna] = scaler.fit_transform(df[[nome_coluna]])
        joblib.dump(scaler, f"./objects/scaler{nome_coluna}.joblib")

    return df

def save_encoders(df, nome_colunas):
    for nome_coluna in nome_colunas:
        label_encoder = LabelEncoder()
        df[nome_coluna] = label_encoder.fit_transform(df[nome_coluna])
        joblib.dump(label_encoder, f"./objects/labelencoder{nome_coluna}.joblib")

    return df
 
            

