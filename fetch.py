import requests
from bs4 import BeautifulSoup
import json

def fetch_from_538(state):
	forecast_page = "http://projects.fivethirtyeight.com/2016-election-forecast/"+state+"/"
	forecast_html = requests.get(forecast_page)
	soup = BeautifulSoup(forecast_html.text, 'html.parser')

	script_tags = soup.find_all("script")

	# Select the correct Script Tag
	javascript_code = script_tags[7].string

	# Find JSON Data
	start = javascript_code.index("race.stateData") + len("race.stateData")
	end   = javascript_code.index("race.pathPrefix", start)
	data_variable = javascript_code[start+3:end-1]

	forecast = json.loads(data_variable)
	return forecast


states = ["alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut",\
          "delaware", "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", \
          "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan",\
          "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "new-hampshire",\
           "new-jersey", "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio", \
           "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina", "south-dakota", \
           "tennessee", "texas", "utah", "vermont", "virginia", "washington", "west-virginia", \
           "wisconsin", "wyoming", "district-of-columbia"]

for state in states:
	forecast_data = fetch_from_538(state)
	with open("polls/" + state + '.txt', 'w') as outfile:
		json.dump(forecast_data['polls'], outfile)
	with open("forecasts/" + state + '.txt', 'w') as outfile:
		json.dump(forecast_data['forecasts']['all'], outfile)
	print state + " Done"
	