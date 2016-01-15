import pandas as pd
import pickle

FILE_NAME = 'data/All_species.json'

def make_species_table(file_name=FILE_NAME):
	data = pd.read_json(file_name)

	counts = data['querySpecificObservationCount']

	aggregated_data = []
	for i, taxa in enumerate(data['taxon']):
	    aggregated_data.append([counts[i], taxa.get('commonName'), taxa['name'],
	     						taxa['organismKey'], taxa['rank'], taxa['gatewayRecordCount']])

	df= pd.DataFrame(aggregated_data)

	df.columns= ['observation_count', 'common_name', 'scientific_name', 'species_key', 'rank', 'record_count']

	df['common_name'][pd.isnull(df['common_name'])]=''
	df['common_name'] = df['common_name'].apply(lambda x: x.encode('ascii', 'ignore'))

	df.to_csv('data/species_table.csv')


if __name__ == "__main__":
    print ('''
    This script takes a json of species data and creates a csv of species information.
    This information is used by the webapp.
    ''')
    raw_input('Press Enter to continue, or control-c to abort...')

    make_species_table()
    