import csv
import calendar
import os

# Caminho da pasta onde os arquivos CSV estão localizados
folder_path = 'venv/csv_files'
# Caminho temporário para salvar os arquivos CSV processados antes de substituir os originais
temp_file_path = 'temp_seu_arquivo.csv'

# Função para adicionar seis linhas a um dado ano
def add_six_lines(data, index, year):
    for _ in range(6):
        # Adiciona uma nova linha com dados especificados
        data.insert(index + 1, [f"{year}-00-00 0:00:00", "-6.64", "-40.6", "0"])
    return data

# Função para adicionar cinco linhas a um dado ano
def add_five_lines(data, index, year):
    for _ in range(5):
        # Adiciona uma nova linha com dados especificados
        data.insert(index + 1, [f"{year}-00-00 0:00:00", "-6.64", "-40.6", "0"])
    return data

# Obtém a lista de todos os arquivos CSV na pasta especificada
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Loop através de cada arquivo CSV encontrado
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        # Lê o conteúdo do arquivo CSV e armazena em uma lista
        data = list(csv_reader)

    # Copia as primeiras quatro linhas (metadados/cabeçalhos)
    new_data = data[:4]  
    last_leap_year = None
    last_non_leap_year = None

    # Loop através das linhas restantes do CSV
    for i, row in enumerate(data[4:], start=4):
        row_str = ''.join(row)
        first_4_chars = row_str[:4]
        
        if first_4_chars.isdigit():
            # Converte os primeiros 4 caracteres do ano em um número inteiro
            year = int(first_4_chars)
            if calendar.isleap(year):
                # Se o ano é bissexto e é diferente do último ano bissexto processado
                if last_leap_year is None or last_leap_year != year:
                    new_data = add_six_lines(new_data, len(new_data) - 1, year)
                new_data.append(row)
                last_leap_year = year
                last_non_leap_year = None
            else:
                # Se o ano não é bissexto e é diferente do último ano não bissexto processado
                if last_non_leap_year is None or last_non_leap_year != year:
                    new_data = add_five_lines(new_data, len(new_data) - 1, year)
                new_data.append(row)
                last_non_leap_year = year
                last_leap_year = None
        else:
            new_data.append(row)

    # Escreve os dados processados em um arquivo temporário
    with open(temp_file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(new_data)

    # Substitui o arquivo original pelo arquivo temporário processado
    os.replace(temp_file_path, file_path)

    print("process concluded")
