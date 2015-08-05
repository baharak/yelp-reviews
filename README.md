# yelp-reviews
The reviews entered by the users are valuable information that can be used for ranking the reviews and physical revenues. So, the first question to answer is how to extract the most information from the available reviews.
Input data: https://www.yelp.com/academic_dataset
time python step1.py tmplIDXQt=dataset  
time python step1.py tmplIDXQt=dataset

time python step2.py reviews.csv -bigram
time python step2.py reviews.csv -unigram

time python step3.py unigramdata.csv smoothing squareloss > uni_ss 
time python step3.py bigramdata.csv smoothing squareloss  > biss 
time python step3.py unigramdata.csv nosmoothing squareloss > uni_ns 
time python step3.py bigramdata.csv nsmoothing squareloss > binss 
