from requests import get
from bs4 import BeautifulSoup
import csv
url = 'https://www.imdb.com/title/tt1837492/episodes?season={}&ref_=tt_eps_sn_{}'

with open('data.csv', 'w', newline='') as file:
    field_names = ['Name', 'Season', 'Review Link', 'Year']
    writer = csv.DictWriter(file, fieldnames = field_names)
    writer.writeheader()
    for x in range(1,5,1):
        response = get(url.format(x, x))
        html_soup = BeautifulSoup(response.text, 'html.parser')
        episodesContainerOdd = html_soup.find_all('div', class_ = 'list_item odd')
        episodesContainerEven = html_soup.find_all('div', class_ = 'list_item even')
        firstEpisode = episodesContainerOdd[0]
        review_link = "https://www.imdb.com{}reviews?ref_=tt_urv"
        secondEpisode = episodesContainerEven[0]
        for i in range(len(episodesContainerOdd)):
            writer.writerow({'Name': episodesContainerOdd[i].strong.text, 'Season': x, 'Review Link': review_link.format(episodesContainerOdd[i].strong.a['href']), 'Year': episodesContainerOdd[i].find('div', class_ = 'airdate').text.split(" ")[14].split("\n")[0]})
            if i < len(episodesContainerEven):
                writer.writerow({'Name': episodesContainerEven[i].strong.text, 'Season': x, 'Review Link': review_link.format(episodesContainerEven[i].strong.a['href']), 'Year': episodesContainerEven[i].find('div', class_ = 'airdate').text.split(" ")[14].split("\n")[0]})

with open('data.csv', 'r', newline='') as file:
    reader = csv.DictReader(file)
    i = 1
    for row in reader:
        review_link = row['Review Link']
        response = get(review_link)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        ratings = html_soup.find_all('span', class_ = 'rating-other-user-rating')
        reviews = html_soup.find_all('div', class_ = 'lister-item-content')
        # print(f"Rating: {len(ratings)}\nReviews: {len(reviews)}\n\n")
        ratings_it = 0
        for review in reviews:
            ratings_exist = review.find('span', class_ = 'rating-other-user-rating')
            if ratings_exist == None:
                continue
            review_text = review.find('div', class_ = 'text show-more__control').text
            score = ratings[ratings_it].span.text
            print(f"\n{i}: Rating: {score}/10\n{review_text}\n")
            ratings_it += 1
            i += 1


# Rating: {review.find('span', class_ = 'rating-other-user-rating').span.text}