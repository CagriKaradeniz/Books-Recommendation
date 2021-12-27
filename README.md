# Books-Recommendation
![This is an image](https://uploads-ssl.webflow.com/5fdc17d51dc102ed1cf87c05/602c3dd964f94d4a9cfa8555_netflix.png)
# Business Problem
During the last few decades, with the rise of Youtube, Amazon, Netflix and many other such web services, recommender systems have taken more and more place in our lives. From e-commerce (suggest to buyers articles that could interest them) to online advertisement (suggest to users the right contents, matching their preferences), recommender systems are today unavoidable in our daily online journeys.

For this sample;

I tried to merge all datasets and analyse them with item based and user based algorithm.
I created one function to give a choice to select item or based algorithm to user.
According to users choice, system is recommending 2 books to user.
# Dataset

The Book-Crossing dataset comprises 3 files. You can reach datasets but this adress (https://www.kaggle.com/arashnic/book-recommendation-dataset)

1.) Users

Contains the users. Note that user IDs (User-ID) have been anonymized and map to integers. Demographic data is provided (Location, Age) if available. Otherwise, these fields contain NULL-values.

2.) Books

Books are identified by their respective ISBN. Invalid ISBNs have already been removed from the dataset. Moreover, some content-based information is given (Book-Title, Book-Author, Year-Of-Publication, Publisher), obtained from Amazon Web Services. Note that in case of several authors, only the first is provided. URLs linking to cover images are also given, appearing in three different flavours (Image-URL-S, Image-URL-M, Image-URL-L), i.e., small, medium, large. These URLs point to the Amazon web site.

3.) Ratings

Contains the book rating information. Ratings (Book-Rating) are either explicit, expressed on a scale from 1-10 (higher values denoting higher appreciation), or implicit, expressed by 0.
