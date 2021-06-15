from requests import get
url = 'https://www.imdb.com/title/tt6468322/episodes?season=1&ref_=tt_eps_sn_1'
response = get(url)
#print(response.text[:500])

from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)


movie_containers = html_soup.find_all('div', class_ = 'article listo list')
#episodes_container = html_soup.find_all('div', class_ = 'info')
episodesContainerOdd = html_soup.find_all('div', class_ = 'list_item odd')
episodesContainerEven = html_soup.find_all('div', class_ = 'list_item even')
#print(type(movie_containers))
#print(len(movie_containers))

firstEpisode = episodesContainerOdd[0]
secondEpisode = episodesContainerEven[0]

#series_name = movie_containers.h3.a.text


first_episode = firstEpisode.strong.text
second_episode = secondEpisode.strong.text

for i in episodesContainerEven:
    print(episodesContainerOdd[len(episodesContainerOdd)-1].strong.text)
    print(episodesContainerEven[len(episodesContainerEven)-1].strong.text)
    len(episodesContainerEven)-1
    len(episodesContainerEven)-1


#for all in episodesContainerOdd:
    #print(episodesContainerOdd.strong.text)
#print(series_name)
#print('Episode 1: ' + first_episode)
#print('Episode 2: ' + second_episode)
#print(len(episodesContainerOdd))
