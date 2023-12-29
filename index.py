import os
import cv2
import pytesseract

#Passando o caminho do tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Função com a logica
def extraindo_numero(caminho_imagem):
    try:
        #lendo o arquivo com o CV2
        canhotinho = cv2.imread(caminho_imagem)

        # Cortando a imagem e pegando o lado direito PS: Regra separada para facilitar a leitura dos numeros a direita dos canhotos
        if canhotinho is not None:
            altura, largura, _ = canhotinho.shape
            metade_largura = largura // 2
            leitura = canhotinho[:, metade_largura:]

            #lendo a imagem com o tesseract
            numeros_extraidos = pytesseract.image_to_string(leitura, lang='por', config='--oem 3 --psm 6 -l por')
            palavras = numeros_extraidos.split()
            
            # tentando encontrar a posição da palavra "No."" ou "No"
            posicao_no = None
            for i, palavra in enumerate(palavras):
                if "No." in palavra or ("No" in palavra and "No." not in palavra):
                    posicao_no = i
                    break

            # Se "No." for encontrado, capturar o próximo elemento
            numero_apos_no = None
            if posicao_no is not None and posicao_no + 1 < len(palavras):
                numero_apos_no = palavras[posicao_no + 1]

            return numero_apos_no #retornando o texto
        else:
            print(f"Erro: Não foi possível ler a imagem: {caminho_imagem}")
    except Exception as err:
        print(f"Erro encontrado: {err}")

# Informando o diretorio das imagens
lista_canhotos = os.listdir("Canhotos")

# Criando o laço de repetição para executar os arquivos
for arquivo in lista_canhotos:
    caminho_arquivo_original = os.path.join(lista_canhotos, arquivo)
    numero_extraido = extraindo_numero(caminho_arquivo_original)

    if numero_extraido:
        # Obtém a extensão original do arquivo
        _, extensao = os.path.splitext(arquivo)
        
        # Constrói o novo nome do arquivo
        novo_nome = f'{numero_extraido}{extensao}'
        
        # Constrói o caminho completo para o novo arquivo
        caminho_novo = os.path.join(lista_canhotos, novo_nome)

        # Verifica se o caminho_novo já existe
        if os.path.exists(caminho_novo):
            pass
        else:
            # Renomeia o arquivo apenas se o novo caminho não existir
            os.rename(caminho_arquivo_original, caminho_novo)

        print(f'Arquivo renomeado: {caminho_novo}')
