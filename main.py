from flask import Flask, request, render_template
import time
from webscrapping import obter_ultimos_filmes
from createcollage import create_collage

app = Flask(__name__, template_folder='./templates', static_folder='./static')

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        username = request.form['username']
        
        start_time = time.time()
        print("Iniciando web scraping...")
        ultimas_imagens, stars_movies, title_movies, year_movies, rewatch_status, review_status = obter_ultimos_filmes(username, quantidade=12)
        web_scraping_time = time.time() - start_time
        print(f"Web scraping concluído em {web_scraping_time:.2f} segundos.")
        
        if ultimas_imagens:
            start_time = time.time()
            print("Iniciando criação da colagem...")
            collage = create_collage(ultimas_imagens, title_movies, stars_movies, year_movies, rewatch_status, review_status)
            collage_creation_time = time.time() - start_time
            print(f"Criação da colagem concluída em {collage_creation_time:.2f} segundos.")
            
            tempo_total = web_scraping_time + collage_creation_time
            print(f"Tempo total de espera: {tempo_total:.2f}")
            
            if collage:
                return render_template('index.html', username=username, quantidade=12, show_image=True)

    return render_template('index.html', show_image=False)


if __name__ == "__main__":
    app.run(debug=True)
