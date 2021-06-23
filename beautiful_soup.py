from enum import unique
from requests import get
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv
import re
import string
import math
url = 'https://www.imdb.com/title/tt1837492/episodes?season={}&ref_=tt_eps_sn_{}'
list_reviews = []
list_words = []


# This class saves all reviews and related information necessary
class Review():
    
    
    def __init__(self, episode_name, text, score):
        self.episode_name = episode_name
        self.text = f"\n{text.lower()}\n"
        self.score = int(score)
        self.status = ''
        self.set_review_status()

    def set_review_status(self):
        self.status = 'negative' if self.score < 8 else 'positive'

# This class saves all word and related information necessary
class Word():

    def __init__(self, word, review_number, review_status, positive_frequency = 0, negative_frequency = 0, positive_reviews = 0, negative_reviews = 0):
        self.text = word
        self.review_number = review_number
        self.review_status = review_status
        self.positive_frequency = positive_frequency
        self.negative_frequency = negative_frequency
        self.positive_reviews = positive_reviews
        self.negative_reviews = negative_reviews
        self.positive_probability = 0
        self.negative_probability = 0 
        self.total_frequency = 0
        if self.negative_frequency == 0 and self.positive_frequency == 0:
            if self.review_status == "positive":
                self.positive_frequency += 1
                self.positive_reviews += 1
            else:
                self.negative_frequency += 1
                self.negative_reviews += 1
            self.set_total_frequency()

    def __eq__(self, other):
        if other != None and self.text == other.text:
            return True
        return False

    def set_total_frequency(self):
        self.total_frequency = self.positive_frequency + self.negative_frequency

    def set_review_number(self, review_number):
        self.review_number = review_number
    
    def set_positive_probability(self, positive_probability):
        self.positive_probability = positive_probability
    
    def set_negative_probability(self, negative_probability):
        self.negative_probability = negative_probability

    def increment_reviews(self, review_number, review_status):
        if self.review_number != review_number:
            self.review_number = review_number
            if review_status == 'positive':
                self.positive_reviews += 1
            else:
                self.negative_reviews += 1

    def increment_frequency(self, review_status):
        if review_status == "positive":
            self.positive_frequency += 1
        else:
            self.negative_frequency += 1

# This is the function that will go through the frequency and provide our infrequent filtering
def infrequent_word_filtering (no_emoji_list, count):

    if count == 0 or count == 1 or count ==2:
        infrequent_list = []   
        for word in no_emoji_list:
            if count == 0 and word.positive_frequency + word.negative_frequency == 1:
                removed_list.append(word)
                infrequent_list.append(word)
            if count == 1 and word.positive_frequency+word.negative_frequency <= 10:
                search_result = search_list(removed_list, word.text)
                if search_result == None:
                    removed_list.append(word) 
                    infrequent_list.append(word)  
            if count == 2 and word.positive_frequency+word.negative_frequency <= 20:
                search_result = search_list(removed_list, word.text)
                if search_result == None:
                    removed_list.append(word)
                    infrequent_list.append(word)
        for word in infrequent_list:
            no_emoji_list.remove(word)               
    if count == 3:
        total = int(len(no_emoji_list)*0.05)
        for x in range(total):
            removed_list.append(no_emoji_list[0])
            no_emoji_list.remove(no_emoji_list[0])
    if count == 4:
        total = int(len(no_emoji_list)*0.1)
        for x in range(total):
            removed_list.append(no_emoji_list[0])
            no_emoji_list.remove(no_emoji_list[0])
    if count == 5:
        total = int(len(no_emoji_list)*0.2)
        for x in range(total):
            removed_list.append(no_emoji_list[0])
            no_emoji_list.remove(no_emoji_list[0])

# This function removes all emojis used in a review (Honestly didn't think this would be an issue)       
def remove_emoji(list_words, return_list, positive_words = 0, negative_words = 0):
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
        if emoji_pattern.sub(r'', word.text) != '':
            return_list.append(Word(emoji_pattern.sub(r'', word.text),word.review_number, word.review_status,positive_frequency =  word.positive_frequency, negative_frequency = word.negative_frequency, positive_reviews=word.positive_reviews, negative_reviews=word.negative_reviews))
    return return_list

# This function will search the list of words and return the word if it exists
def search_list(list_words, text):
    for word in list_words:
        if word.text == text:
            return word
    return None

# This function removes all words of length 2 or less
def lengthLessThan2(no_emoji_list, removed_list):
    new_list = []
    for word in no_emoji_list:
        if len(word.text) <= 2:
            removed_list.append(word)
            new_list.append(word)
    for word in new_list:
        no_emoji_list.remove(word)

# This function removes all words of length 4 or less
def lengthLessThan4(no_emoji_list, removed_list):
    new_list = []
    for word in no_emoji_list:
        if len(word.text) <= 4:
            search_result = search_list(removed_list, word.text)
            if search_result == None:
                removed_list.append(word)
                new_list.append(word)
    for word in new_list:
        no_emoji_list.remove(word)

# This function removes all words of length 9 or greater
def lengthGreaterThan9(no_emoji_list, removed_list):
    new_list = []
    for word in no_emoji_list:
        if len(word.text) >= 9:
            removed_list.append(word)
            new_list.append(word)
    for word in new_list:
        no_emoji_list.remove(word)

# This function will decided which length filtering to run
def lengthFiltering(count, no_emoji_list, removed_list):
    if count == 0:
        lengthLessThan2(no_emoji_list, removed_list)
    if count == 1:
        lengthLessThan4(no_emoji_list, removed_list)
    if count == 2:
        lengthGreaterThan9(no_emoji_list, removed_list)

# This will setup configurations for smoothing, frequency filtering, and length filtering
smoothing = int(input("Would you like to run smoothing? "))
while smoothing != 0 and smoothing != 1:
    smoothing = int(input("Would you like to run smoothing? Enter 1 for yes 0 for no"))
if smoothing == 0:
    smoothing_factors = [1]
else:
    smoothing_factors = [1, 1.2, 1.4, 1.6, 1.8, 2.0]

infrequent_filtering = int(input("Would you like to run infrequent filtering? "))
while infrequent_filtering != 0 and infrequent_filtering != 1:
    infrequent_filtering = int(input("Would you like to run infrequent filtering. Enter 1 for yes 0 for no"))
if infrequent_filtering == 0:
    infrequent_factors = [0]
else:
    infrequent_factors = [0, 1, 2, 3, 4, 5]

length_filtering  = int(input("Would you like to run length filtering? "))
while length_filtering != 0 and length_filtering != 1:
    length_filtering = int(input("Would you like to run length filtering? Enter 1 for yes 0 for no"))
if length_filtering == 0:
    length_filtering_factors = [0]
else:
    length_filtering_factors = [0, 1, 2]

# This will create the data.csv file
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
positive_reviews = []
negative_reviews = []

# This will open every review and save them as either positive or negative reviews
with open('data.csv', 'r', newline='') as file:
    reader = csv.DictReader(file)
    i = 1
    for row in reader:
        review_link = row['Review Link']
        episode_name = row['Name']
        response = get(review_link)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        ratings = html_soup.find_all('span', class_ = 'rating-other-user-rating')
        reviews = html_soup.find_all('div', class_ = 'lister-item-content')
        ratings_it = 0
        for review in reviews:
            ratings_exist = review.find('span', class_ = 'rating-other-user-rating')
            if ratings_exist == None:
                continue
            review_text = review.find('div', class_ = 'text show-more__control').text
            score = ratings[ratings_it].span.text
            full_review = Review(episode_name, review_text, score)
            positive_reviews.append(full_review) if full_review.status == 'positive' else negative_reviews.append(full_review)
            list_reviews.append(full_review)
            ratings_it += 1
            i += 1
review_number = 1
positive_words = 0
negative_words = 0

# Half the test data is created from half positive reviews
for i in range(int(len(positive_reviews)/2)):
    review = positive_reviews[i]
    words = re.sub('['+string.punctuation+']', '', review.text).split()
    for word in words:
        search_result = search_list(list_words, word)
        if search_result != None:
            search_result.increment_frequency(review.status)
            search_result.increment_reviews(review_number, review.status)
        else:
            list_words.append(Word(word, review_number, review.status))
    review_number += 1
pr_number = review_number-1
review_number = 1

# Half the test data is created from negative reviews
for i in range(int(len(negative_reviews)/2)):
    review = negative_reviews[i]
    words = re.sub('['+string.punctuation+']', '', review.text).split()
    for word in words:
        search_result = search_list(list_words, word)
        if search_result != None:
            search_result.increment_frequency(review.status)
            search_result.increment_reviews(review_number, review.status)
        else:
            list_words.append(Word(word, review_number, review.status))
    review_number += 1
nr_number = review_number-1
total_md_review = nr_number + pr_number
no_emoji_list = remove_emoji(list_words, [])
removed_list = []
count = 1
remaining_words = []
accuracy = []

# This will run all the filtering entered by the user
for infrequent_counter in infrequent_factors:
    if infrequent_filtering == 0 and length_filtering == 0:
        for word in no_emoji_list:
            if word.positive_frequency + word.negative_frequency < 3:
                removed_list.append(word)
        for word in removed_list:
            no_emoji_list.remove(word)
    if infrequent_filtering == 1:
        no_emoji_list.sort(key=lambda word: word.total_frequency, reverse=True)
        infrequent_word_filtering(no_emoji_list, infrequent_counter)
    no_emoji_list.sort(key=lambda word: word.text, reverse=False)
    removed_list.sort(key=lambda word: word.text, reverse=False)
    for counter in length_filtering_factors:
        if length_filtering == 1:
            lengthFiltering(counter, no_emoji_list, removed_list)
        positive_words = 0
        negative_words = 0
        for word in no_emoji_list:
            positive_words += word.positive_frequency
            negative_words += word.negative_frequency
        for smoothing_factor in smoothing_factors:
            num_words = 1
            prediction_correctness = 0
            if smoothing == 1 and smoothing_factor == 1.6:
                model_file = 'smooth-model.txt'
                result_file = "smooth-result.txt"
            elif infrequent_counter == 5:
                model_file = "frequency-model.txt"
                result_file = "frequency-result.txt"
            elif counter == 2:
                model_file = "length-model.txt"
                result_file = "length-result.txt"
            else:
                model_file = 'model.txt'
                result_file = 'result.txt'
            with open(model_file, 'w', newline='') as file:
                for word in no_emoji_list:
                    word.set_positive_probability((word.positive_frequency+smoothing_factor)/(positive_words+(smoothing_factor*len(no_emoji_list))))
                    word.set_negative_probability((word.negative_frequency+smoothing_factor)/(negative_words+(smoothing_factor*len(no_emoji_list))))
                    file.write(f"No.{num_words} {word.text}\n{word.positive_frequency}, {word.positive_probability}\n{word.negative_frequency}, {word.negative_probability}\n\n")
                    num_words += 1
            num_words = 1
            with open('remove.txt', 'w', newline='') as file:
                for word in removed_list:
                    file.write(f"{word.text}\n")
                    num_words += 1
            total_test_review = 0
            with open(result_file, 'w', newline='') as file:
                for i in range(pr_number, int(len(positive_reviews)), 1):
                    positive_probability = math.log10(pr_number/total_md_review)
                    negative_probability = math.log10(nr_number/total_md_review)
                    review = positive_reviews[i]
                    words = re.sub('['+string.punctuation+']', '', review.text).split()
                    for word in words:
                        search_word = search_list(no_emoji_list, word)
                        if search_word != None:
                            positive_probability += math.log10(search_word.positive_probability)
                            negative_probability += math.log10(search_word.negative_probability)
                        else:
                            positive_probability += math.log10(smoothing_factor)/(positive_words+(smoothing_factor*len(no_emoji_list)))
                            negative_probability += math.log10(smoothing_factor)/(negative_words+(smoothing_factor*len(no_emoji_list)))
                    result = "positive" if positive_probability >= negative_probability else "negative"
                    prediciton_result = "right" if result == review.status else "wrong"
                    if prediciton_result == "right":
                        prediction_correctness += 1
                    file.write(f"No.{total_test_review} {review.episode_name}\n{positive_probability}, {negative_probability}, {result}, {review.status}, {prediciton_result}\n\n")
                    total_test_review += 1
                for i in range(nr_number, int(len(negative_reviews)), 1):
                    positive_probability = math.log10(pr_number/total_md_review)
                    negative_probability = math.log10(nr_number/total_md_review)
                    review = negative_reviews[i]
                    words = re.sub('['+string.punctuation+']', '', review.text).split()
                    for word in words:
                        search_word = search_list(no_emoji_list, word)
                        if search_word != None:
                            positive_probability += math.log10(search_word.positive_probability)
                            negative_probability += math.log10(search_word.negative_probability)
                        else:
                            positive_probability += math.log10((smoothing_factor)/(positive_words+(smoothing_factor*len(no_emoji_list))))
                            negative_probability += math.log10((smoothing_factor)/(negative_words+(smoothing_factor*len(no_emoji_list))))
                    result = "positive" if positive_probability >= negative_probability else "negative"
                    prediciton_result = "right" if result == review.status else "wrong"
                    if prediciton_result == "right":
                        prediction_correctness += 1
                    file.write(f"No.{total_test_review} {review.episode_name}\n{positive_probability}, {negative_probability}, {result}, {review.status}, {prediciton_result} \n\n")
                    total_test_review += 1
                prediction = (prediction_correctness*100)/total_test_review
                file.write(f"The prediciton correctness is: {prediction}")
            remaining_words.append(len(no_emoji_list))
            accuracy.append(prediction)
            count += 1

# This will determine which graph to plot
if smoothing == 1:
    fig, ax = plt.subplots()
    ax.plot(smoothing_factors, accuracy)
    ax.set(xlabel = "Smoothing Factor" , ylabel = "Accuracy", title = "Smoothing vs. Accuracy")
    ax.grid()
    plt.show()
elif infrequent_filtering == 1:
    fig, ax = plt.subplots()
    ax.plot(remaining_words, accuracy)
    ax.set(xlabel = "Words Remaining" , ylabel = "Accuracy", title = " Frequency Filtering vs. Accuracy")
    ax.grid()
    plt.show()
elif length_filtering == 1:
    fig, ax = plt.subplots()
    ax.plot(remaining_words, accuracy)
    ax.set(xlabel = "Words Remaining" , ylabel = "Accuracy", title = " Length Filtering vs. Accuracy")
    ax.grid()
    plt.show()
