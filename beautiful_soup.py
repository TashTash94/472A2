from requests import get
from bs4 import BeautifulSoup
url = 'https://www.imdb.com/title/tt1837492/episodes?season={}&ref_=tt_eps_sn_{}'

for x in range(1,5,1):
    response = get(url.format(x, x))
    html_soup = BeautifulSoup(response.text, 'html.parser')
    episodesContainerOdd = html_soup.find_all('div', class_ = 'list_item odd')
    episodesContainerEven = html_soup.find_all('div', class_ = 'list_item even')
    firstEpisode = episodesContainerOdd[0]
    review_link = "https://www.imdb.com{}reviews?ref_=tt_urv"
    print(f"Season {x}")
    secondEpisode = episodesContainerEven[0]
    for i in range(len(episodesContainerOdd)):
        print(episodesContainerOdd[i].strong.text)
        print(episodesContainerOdd[i].find('div', class_ = 'airdate').text.split(" ")[14].split("\n")[0])
        print(review_link.format(episodesContainerOdd[i].strong.a['href']))
        print('\n')
        if i < len(episodesContainerEven):
            print(episodesContainerEven[i].strong.text)
            print(episodesContainerOdd[i].find('div', class_ = 'airdate').text.split(" ")[14].split("\n")[0])
            print(review_link.format(episodesContainerEven[i].strong.a['href']))
            print('\n')