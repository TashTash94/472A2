from enum import unique
from requests import get
from bs4 import BeautifulSoup
import csv
import re
import string
url = 'https://www.imdb.com/title/tt1837492/episodes?season={}&ref_=tt_eps_sn_{}'
list_reviews = []
list_words = []

def remove_emoji(list_words, return_list):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    for word in list_words:
        return_list.append(emoji_pattern.sub(r'', word))
    return return_list

class Review():

    def __init__(self, text, score):
        self.text = f"\n{text.lower()}\n"
        self.score = int(score)
        self.status = ''
        self.set_review_status()

    def set_review_status(self):
        self.status = 'negative' if self.score < 8 else 'positive'

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
            full_review = Review(review_text, score)
            list_reviews.append(full_review)
            ratings_it += 1
            i += 1
positive_reviews = []
negative_reviews = []
for review in list_reviews:
    positive_reviews.append(review) if review.status == 'positive' else negative_reviews.append(review)
    words = re.sub('['+string.punctuation+']', '', review.text).split()
    for word in words:
        list_words.append(word)
list_words.sort()
no_emoji_list = remove_emoji(list_words, [])

