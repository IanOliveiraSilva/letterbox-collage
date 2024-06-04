from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import textwrap
import numpy as np
from tqdm import tqdm

def add_bottom_gradient(image, min_alpha=0.1):
    np_image = np.array(image).astype(np.float64)
    
    height, width, _ = np_image.shape
    gradient = np.linspace(1, min_alpha, height)[:, np.newaxis]
    
    np_image[:, :, :] *= gradient[:,:,np.newaxis]
    
    np_image = np.clip(np_image, 0, 255)
    
    gradient_image = Image.fromarray(np.uint8(np_image))
    
    return gradient_image

def create_collage(imagens_urls, titulos, classificacoes, year_movies, rewatch_status, review_status, largura_thumb=230, altura_thumb=345, colunas=4, linhas=3):
    max_fotos = colunas * linhas
    imagens_urls = imagens_urls[:max_fotos]
    titulos = titulos[:max_fotos]
    classificacoes = classificacoes[:max_fotos]
    year_movies = year_movies[:max_fotos]
    rewatch_status = rewatch_status[:max_fotos]
    review_status = review_status[:max_fotos]

    largura = colunas * largura_thumb
    altura = linhas * altura_thumb

    collage = Image.new('RGB', (largura, altura), (255, 255, 255))

    rewatch_icon = Image.open("rewatchicon.png").resize((25, 25), Image.LANCZOS)
    review_icon = Image.open("reviewicon.png").resize((20, 20), Image.LANCZOS)

    font = ImageFont.truetype("EleganteClassica.ttf", 20, encoding="unic")
    font2 = ImageFont.truetype("OpenSansEmoji.ttf", 27, encoding="unic")

    for index, (url, titulo, classificacao, rewatch, review, year) in tqdm(enumerate(zip(imagens_urls, titulos, classificacoes, rewatch_status, review_status, year_movies)), total=max_fotos, desc="Criando Colagem"):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((largura_thumb, altura_thumb), Image.LANCZOS)
        img = ImageOps.expand(img, fill='black')

        img = add_bottom_gradient(img)

        draw = ImageDraw.Draw(img)

        shadow_offset = (1.2, 1.2)

        draw.text((10 + shadow_offset[0], altura_thumb - 40 + shadow_offset[1]), classificacao, fill='black', font=font2)
        draw.text((10, altura_thumb - 40), classificacao, fill='#00c42f', font=font2)

        title_lines = textwrap.wrap(f"{titulo} ({year})", width=20)
        title_text = '\n'.join(title_lines)

        draw.text((10, altura_thumb - 80), title_text, fill='white', font=font)

        if rewatch == 'rewatch':
            img.paste(rewatch_icon, (largura_thumb - 60, altura_thumb - 35), rewatch_icon)

        if review == 'review':
            img.paste(review_icon, (largura_thumb - 30, altura_thumb - 32), review_icon)

        x = (index % colunas) * largura_thumb
        y = (index // colunas) * altura_thumb
        collage.paste(img, (x, y))

    collage_path = './static/collage.jpg'
    collage.save(collage_path)
    return collage_path
