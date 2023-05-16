# ImmoWeb Data scraping
N.B:This project is part of the BOUMAN-6 Data Analyst/AI BeCode track. It aims at implementing data scraping on houses posted on immoweb.com

## Running the script:
Executing src/main.py runs a data scraping on real estate posts on immoweb.com. Relevant data is then stored in a .csv in your repository. The script is set to try and fetch posts from 9990 houses on the market. Update the "no_of_urls" settings to your liking, up to 20000, to get more data, possibly including appartments if data is lacking on immoweb.com . Keep in mind part of the data is very bad quality and is discarded.
A regular environment should scrape about 500 properties a minute.
## Installation
Check requirements.txt to make sure your environment has the required packages.
Mainly, the script uses these libraries:

- requests
- json
- beautifulsoup4
- typing
- concurrent.futures
- pandas
- numpy

Clone the repository and run src/main.py 

## Authors:
Credit goes to **Kardiç Said**,**Mirzayev Dastan**, **Subramani Sivasankari** and **Hupin Grégoire**.
  
