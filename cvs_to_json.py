import pandas as pd
import json

df = pd.read_csv('imdb_top_1000.csv')

df.to_json('movies.json', orient='records')

with open('movies.json', 'r') as file:
    movies = json.load(file)

for i in range (100):
    movie = movies[i]
    print(movie)
    break

