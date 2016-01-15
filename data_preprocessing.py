import pandas as pd
import pickle
import matplotlib.pyplot as plt
import graphlab

##Global Variables

PREFIX_FILENAME = 'data/gridsquareprefixescombined.csv' 
    #alternate prefixes include:
        #Great Britain 'data/gridsquareprefixesGB.csv' 
        #Ireland: 'data/gridsquareprefixesIreland.csv'
TARGET_DIRECTORY = 'data/'      #For saving the file
SAVE_FILE_NAME = 'survey_proportion.sframe'

def _all_sites_in_region(region_prefix):
    sites= []
    for i in xrange(10):
        for j in xrange(10):
            sites.append(region_prefix+str(i)+str(j))
    return sites


def _load_data(prefix, directory='data/', suffix='_taxon_data.pkl'):
    file_name = directory+prefix+suffix
    region_taxon_data = pickle.load(open(file_name, "rb" ))
    return region_taxon_data

def _make_data_row(site, taxon_entry, proportional, max_count):
    new_row = None
    if proportional:
        new_row = [site,
                   taxon_entry['taxon']['name'],
                   float(taxon_entry['querySpecificObservationCount'])/max_count
                   ]
    else:
        new_row = [site,
                   taxon_entry['taxon']['name'],
                   1
                   ]
    return new_row



def _trim_data(data, fill, min_locations, min_taxa, presence_threshold):
    ''' Trim data will remove taxa which occur at fewer than min_locations sites, and
        sites which contain fewer than min_taxa taxa. presence_threshold defines the
        proportion, above which, a species is defined to be 'present' in a location, 
        for purposes of counting how many species occurs in for min_locations. '''
    data_df = data.to_dataframe()
    lookup_table = data_df.pivot_table(values= data.column_names()[2], index='site',
                                       columns='taxa', fill_value=fill)
    temp = lookup_table > presence_threshold
    common_taxa_mask= temp.sum(axis=0) >= min_locations
    biodiverse_mask = temp.sum(axis=1) >= min_taxa
    trimmed_lookup_table = lookup_table[biodiverse_mask].T[common_taxa_mask].T
    trimmed_df = trimmed_lookup_table.T.unstack(0).reset_index()
    null_filter = pd.isnull(trimmed_df[0])
    trimmed_df = trimmed_df[~null_filter]
    return graphlab.SFrame(trimmed_df)



#The following converts the data into a single file containing species,
#sites, and the proportion of surveys at that site in which the species occurs.
#Trim data will remove taxa which occur at fewer than min_locations sites, and
#sites which contain fewer than min_taxa taxa. presence_threshold defines the
#proportion, above which, a species is defined to be 'present' in a location, 
#for purposes of counting how many species occurs in for min_locations.

def process_data(prefix_filename, target_directory, save_file_name, proportional=True, trim_data = True,
                 min_locations = 3, min_taxa=100, presence_threshold = 0):
    prefixes = pd.read_csv(prefix_filename, header=None, na_filter=False)[0]
    aggregated_data = []
    for prefix in prefixes:
        print prefix
        region_taxon_data = _load_data(prefix)
        sites = _all_sites_in_region(prefix)
        for site in sites:
            max_count = 0.
            for l in xrange(len(region_taxon_data[site])):
                if region_taxon_data[site][l]['querySpecificObservationCount']> max_count:
                    max_count = float(region_taxon_data[site][l]['querySpecificObservationCount'])

            for taxon in region_taxon_data[site]:
                aggregated_data.append(_make_data_row(site, taxon, proportional, max_count))

    df = pd.DataFrame(aggregated_data)

    #Adding headers
    if proportional:
        headers = ['site', 'taxa', '%present']
        df.columns = headers
        return_df = df[['site', 'taxa', '%present']]
        fill=None
    else:
        headers = ['site', 'taxa', 'present']
        df.columns = headers
        return_df = df[['site', 'taxa', 'present']]
        fill=None

    data_sf = graphlab.SFrame(return_df)

    #
    if trim_data == True:
        data_sf = _trim_data(data_sf, fill, min_locations, min_taxa, presence_threshold)
        #Replace headers
        if proportional:
            headers = {'site':'site', 'taxa':'taxa', '0':'%present'}
            data_sf.rename(headers)
            return_df = df[['site', 'taxa', '%present']]
            fill=None
        else:
            headers = {'site':'site', 'taxa':'taxa', '0':'present'}
            data_sf.rename(headers)
            return_df = df[['site', 'taxa', 'present']]
            fill=None


    save_file_name = target_directory + save_file_name
    data_sf.save(save_file_name)

if __name__ == "__main__":
    print ('''
    This script convert a batch of files produced by data_fetching.py 
    into a single sframe file. This process can take a little while.
    ''')
    raw_input('Press Enter to continue, or control-c to abort...')
    
    process_data(PREFIX_FILENAME, TARGET_DIRECTORY, 'survey_proportion.sframe', proportional= True, 
                 trim_data = True, min_locations = 3, min_taxa=100)

    process_data(PREFIX_FILENAME, TARGET_DIRECTORY, 'presence_absence.sframe', proportional= False,
                 trim_data = True, min_locations = 3, min_taxa=100)



