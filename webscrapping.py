from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm

def obter_ultimos_filmes(username, quantidade=12):
    url = f"https://letterboxd.com/{username}/films/diary/"
    navigator_opt = webdriver.EdgeOptions()
    navigator_opt.add_experimental_option("detach", True)
    navigator_opt.add_argument("--headless")
    
    driver = webdriver.Edge(options=navigator_opt)
    driver.get(url)

    filme_elements = driver.find_elements(By.CSS_SELECTOR, ".diary-entry-row")

    imagens_filmes = []
    stars_movies = []
    title_movies = []
    year_movies = []
    rewatch_status = []
    review_status = []

    for filme in filme_elements[:quantidade]:
        # Imagens
        img_element = filme.find_element(By.CSS_SELECTOR, ".film-poster img")
        imagens_filmes.append(img_element.get_attribute("src").replace("-0-35-0-52", "-0-230-0-345"))

        # Ratings
        stars_element = filme.find_element(By.CSS_SELECTOR, ".td-rating span")
        stars_movies.append(stars_element.text.strip())

        # Títulos
        title_element = filme.find_element(By.CSS_SELECTOR, ".film-poster")
        title_movies.append(title_element.get_attribute("data-film-name"))

        # Anos
        year_element = filme.find_element(By.CSS_SELECTOR, ".film-poster")
        year_movies.append(year_element.get_attribute("data-film-release-year"))

        # Rewatch status
        rewatch_element = filme.find_element(By.CSS_SELECTOR, ".td-rewatch")
        rewatch_status.append('rewatch' if 'icon-status-off' not in rewatch_element.get_attribute('class') else 'first-watch')

        # Review status
        review_element = filme.find_element(By.CSS_SELECTOR, ".td-review")
        review_status.append('review' if 'icon-status-off' not in review_element.get_attribute('class') else 'no-review')

    driver.quit()

    return imagens_filmes, stars_movies, title_movies, year_movies, rewatch_status, review_status
