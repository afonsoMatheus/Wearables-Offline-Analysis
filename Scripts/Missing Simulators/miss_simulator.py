import pandas as pd
import numpy as np
from mdatagen.univariate.uMCAR import uMCAR
import os
import argparse

# Configurar argumentos de linha de comando
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Simulador de valores ausentes em datasets.")
    parser.add_argument(
        "-m", 
        type=str, 
        required=True, 
        choices=["MCAR", "MAR", "MNAR"], 
        help="Nome do mecanismo de missing data (escolha entre: MCAR, MAR, MNAR)."
    )
    parser.add_argument("-p", type=int, required=True, help="Porcentagem de valores ausentes (ex: 25, 50, ...).")
    parser.add_argument("-n", type=int, required=True, help="Número de datasets a serem gerados para cada arquivo.")

    # Parsear os argumentos
    args = parser.parse_args()

    # Atribuir os argumentos a variáveis
    mechanism = args.m
    mr = args.p
    num_datasets = args.n

    # Caminho da pasta
    folder_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'COVID-19-Wearables')

    # Listar todos os arquivos na pasta
    files = [file for file in os.listdir(folder_path) if file.endswith('_hr.csv')]

    for file_name in files:
        # Caminho completo do arquivo
        file_path = os.path.join(folder_path, file_name)
        
        # Carregar o arquivo CSV como um DataFrame
        try:
            data = pd.read_csv(file_path)
        except Exception as e:
            print(f"Erro ao carregar o arquivo {file_name}: {e}")
            continue

        for idx in range(1, num_datasets + 1):
            match mechanism:
                case "MCAR":
                    X = data[["datetime", "heartrate"]]
                    X.set_index("datetime", inplace=True)

                    # Criar uma instância com taxa de missing igual a 25% no dataset sob o mecanismo MCAR
                    generator = uMCAR(X=X, y=data.heartrate.to_numpy(), missing_rate=mr, x_miss="heartrate") 
                    
                    # Gerar os dados com valores ausentes
                    generate_data = generator.random()

                case "MAR":
                    # Implementar o mecanismo MAR aqui
                    pass

                case "MNAR":
                    # Implementar o mecanismo MNAR aqui
                    pass

                case _:
                    print(f"Mecanismo {mechanism} inválido.")
                    continue
                
            # Caminho para salvar o novo dataset
            # Criar pastas baseadas no MCAR e na porcentagem
            base_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'COVID-19-Wearables-Missing')
            mcar_folder = os.path.join(base_folder, mechanism)
            percentage_folder = os.path.join(mcar_folder, f'{mr}')
            idx_folder = os.path.join(percentage_folder, f'{idx}')

            os.makedirs(idx_folder, exist_ok=True)

            # Caminho para salvar o novo dataset
            save_path = os.path.join(idx_folder, file_name.replace('.csv', f'_{mechanism}_{mr}_{idx}.csv'))
            
            # Salvar o novo dataset com valores ausentes
            generate_data.reset_index().merge(data[["datetime", "user"]], on="datetime")[["user", "datetime", "heartrate", "target"]].to_csv(save_path, index=False)

            print(f"✅ Arquivo {file_name} dataset {idx} processado e salvo como {save_path}")

    # Exibir mensagem de conclusão
    print("✅ Todos os arquivos foram processados e salvos com sucesso.")
