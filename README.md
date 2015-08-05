# yelp-reviews
The reviews entered by the users are valuable information that can be used for ranking the reviews and physical revenues. So, the first question to answer is how to extract the most information from the available reviews.
Input data: https://www.yelp.com/academic_dataset

To Run the steps:

time python step1.py dataset  

The output of step1 is a reviews.csv in csv format

time python step2.py reviews.csv -bigram
time python step2.py reviews.csv -unigram

The output of step2 is a data.csv file in csv format
Based on the unigram or bigram features; it will be names:
unigramdata.csv or bigramdata.csv

For step3, can have the option of smoothing or no smoothign with --nosmoothing;

time python step3.py data.csv smoothing squareloss 


