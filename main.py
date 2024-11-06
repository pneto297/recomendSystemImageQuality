import os
from PIL import Image
import numpy as np
import cv2

# Definindo as faixas ideais para cada parâmetro
BRILHO_IDEAL = (80, 150)
CONTRASTE_IDEAL = 30
NITIDEZ_IDEAL = 400
RUIDO_IDEAL = 50
FOCO_IDEAL = 500  # Ajuste este valor com base em testes para seu contexto

# Função para calcular os parâmetros de qualidade da imagem
def calcular_qualidade(imagem):
    # Converte a imagem para escala de cinza
    imagem_gray = np.array(imagem.convert("L"))

    # Calcula o brilho (média dos pixels)
    brilho = np.mean(imagem_gray)

    # Calcula o contraste (desvio padrão dos pixels)
    contraste = np.std(imagem_gray)

    # Calcula a nitidez usando a variância do Laplaciano
    nitidez = cv2.Laplacian(imagem_gray, cv2.CV_64F).var()

    # Calcula o ruído (variação local)
    ruido = np.std(imagem_gray - cv2.GaussianBlur(imagem_gray, (5, 5), 0))

    return brilho, contraste, nitidez, ruido

# Função para gerar recomendações com base nos parâmetros
def gerar_recomendacoes(brilho, contraste, nitidez, ruido):
    recomendacoes = []

    if brilho < BRILHO_IDEAL[0]:
        recomendacoes.append(("Aumentar o brilho para melhorar a visibilidade.", "Increase brightness to improve visibility."))
    elif brilho > BRILHO_IDEAL[1]:
        recomendacoes.append(("Reduzir o brilho para evitar sobreexposição.", "Reduce brightness to avoid overexposure."))

    if contraste < CONTRASTE_IDEAL:
        recomendacoes.append(("Aumentar o contraste para melhorar a diferenciação de objetos.", "Increase contrast to enhance object differentiation."))

    if nitidez < NITIDEZ_IDEAL:
        recomendacoes.append(("Ajustar o foco ou aumentar a resolução para melhorar a nitidez.", "Adjust focus or increase resolution to improve sharpness."))

    if ruido > RUIDO_IDEAL:
        recomendacoes.append(("Aplicar filtro de redução de ruído ou melhorar a iluminação.", "Apply noise reduction filter or improve lighting."))

    if not recomendacoes:
        recomendacoes.append(("A imagem está dentro dos parâmetros ideais de qualidade.", "The image is within ideal quality parameters."))

    return recomendacoes

# Função para verificar se a imagem está em foco
def verificar_foco(nitidez):
    if nitidez < FOCO_IDEAL:
        return ("Imagem pode estar fora de foco. Considere ajustar a lente ou posição da câmera.",
                "Image may be out of focus. Consider adjusting the lens or camera position.")
    return ("Imagem está em foco.", "Image is in focus.")

pasta_imagens = 'sample_test'

# Loop para processar cada imagem na pasta
for nome_arquivo in os.listdir(pasta_imagens):
    caminho_imagem = os.path.join(pasta_imagens, nome_arquivo)

    # Verifica se é um arquivo de imagem
    if caminho_imagem.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Carrega a imagem
        imagem = Image.open(caminho_imagem)

        # Calcula os parâmetros de qualidade
        brilho, contraste, nitidez, ruido = calcular_qualidade(imagem)

        # Gera as recomendações
        recomendacoes = gerar_recomendacoes(brilho, contraste, nitidez, ruido)
        foco_recomendacao = verificar_foco(nitidez)

        # Exibe o resultado
        print(f"Imagem: {nome_arquivo}")
        print(f"Brilho: {brilho:.2f}, Contraste: {contraste:.2f}, Nitidez: {nitidez:.2f}, Ruído: {ruido:.2f}")
        print("Recomendações:")
        for rec in recomendacoes:
            print(f" - {rec[0]} (Português) / {rec[1]} (English)")
        print(f" - {foco_recomendacao[0]} (Português) / {foco_recomendacao[1]} (English)")
        print("\n" + "=" * 50 + "\n")
