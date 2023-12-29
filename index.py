import os
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def extraindo_numero(caminho_imagem):
    try:
        canhotinho = cv2.imread(caminho_imagem)

        # Verifica se a leitura da imagem foi bem-sucedida
        if canhotinho is not None:
            altura, largura, _ = canhotinho.shape
            metade_largura = largura // 2
            leitura = canhotinho[:, metade_largura:]

            numeros_extraidos = pytesseract.image_to_string(leitura, lang='por', config='--oem 3 --psm 6 -l por')
            palavras = numeros_extraidos.split()
            print(palavras)

            # Encontrar a posição da palavra "No."
            posicao_no = None
            for i, palavra in enumerate(palavras):
                if "No." in palavra or ("No" in palavra and "No." not in palavra):
                    posicao_no = i
                    break

            # Se "No." for encontrado, capturar o próximo elemento
            numero_apos_no = None
            if posicao_no is not None and posicao_no + 1 < len(palavras):
                numero_apos_no = palavras[posicao_no + 1]

            return numero_apos_no
        else:
            print(f"Erro: Não foi possível ler a imagem: {caminho_imagem}")
            return None

    except Exception as err:
        print(f"Erro encontrado: {err}")
        return None

# Carregando a imagem
diretorio_canhotos = "Canhotos"
lista_canhotos = os.listdir(diretorio_canhotos)

for arquivo in lista_canhotos:
    caminho_arquivo_original = os.path.join(diretorio_canhotos, arquivo)
    numero_extraido = extraindo_numero(caminho_arquivo_original)

    if numero_extraido:
        # Obtém a extensão original do arquivo
        _, extensao = os.path.splitext(arquivo)
        
        # Constrói o novo nome do arquivo
        novo_nome = f'{numero_extraido}{extensao}'
        
        # Constrói o caminho completo para o novo arquivo
        caminho_novo = os.path.join(diretorio_canhotos, novo_nome)

        # Verifica se o caminho_novo já existe
        if os.path.exists(caminho_novo):
            pass
        else:
            # Renomeia o arquivo apenas se o novo caminho não existir
            os.rename(caminho_arquivo_original, caminho_novo)

        print(f'Arquivo renomeado: {caminho_novo}')
