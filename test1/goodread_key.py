import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "wGl6R3MomAtyu1Uur0Sbw", "isbns": "9781632168146"})
print(res.json())