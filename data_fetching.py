import pandas as pd
import urllib
import json
import pickle

##Global Variables

PREFIX_FILENAME = 'data/gridsquareprefixescombined.csv' 
    #alternate prefixes include:
        #Great Britain 'data/gridsquareprefixesGB.csv' 
        #Ireland: 'data/gridsquareprefixesIreland.csv'
TAXON_CODE = 'NHMSYS0000080054'                         
    #Codes include:
        #Flowering Plants: 'NHMSYS0000080054' 
        #Conifers: 'NHMSYS0000080047'
        #Birds: 'NHMSYS0000080039'
        #Beetles: 'NHMSYS0000080066'
        #Butterflies: 'NHMSYS0000080067'
        #See https://data.nbn.org.uk/Taxa for more.
TARGET_DIRECTORY = 'data/'


##Functions

def _build_url(site_code, taxon_code):
    '''
    this should return a url that links to a json that contains a list of a 
    species which occur in the quadrat specified by the prefix and suffix. 
    '''
    url = 'https://data.nbn.org.uk/api/taxonObservations/species/?startYear=\
           &endYear=&spatialRelationship=overlap&designation=&\
           nbn-species-table_length=25&datasetKey=&featureID='+site_code+\
           '&taxonOutputGroup='+taxon_code
    return url


#Load the list of site prefixes. This file can be modified to specify which 
#100x100km grids to use for analysis. Prefix files exist for Ireland, the rest of the British
#Isles and the entirety of the British Isles.

def download_files(prefix_filename, taxon_code, target_directory, start_prefix = 0):
    #This will produce of files containing the raw downloaded data organized
    # by 100x100 km regions. Each region contains data for 100 10x10km sites.
    #This process takes awhile and will frequently fail. If and when it does, the
    #process can be resumed where it broke by replacing the value for start_prefix
    #with the last value printed out.

    prefix_list= pd.read_csv(prefix_filename, header=None, na_filter=False)[0]

    counter = start_prefix
    for prefix in prefix_list[start_prefix:]:
        site_list=[]
        for i in xrange(0,10):
            for j in xrange(0,10):
                site_list.append(prefix+str(i)+str(j))
        url_list = []
        for site in site_list:
            url_list.append(_build_url(site, taxon_code))
            
        url_list = [_build_url(site, taxon_code) for site in site_list]
            
        site_json_strings = []
        for url in url_list:
            site_json = urllib.urlopen(url)
            site_json_strings.append(site_json.read())
        
        site_dict = {}
        for i, site in enumerate(site_list):
            site_dict[site]=json.loads(site_json_strings[i])
        
        file_name = target_directory+prefix+'_taxon_data.pkl'
        pickle.dump(site_dict, open(file_name, 'wb'))
        
        print 'resume at number:', counter
        print 'last file saved:', file_name
        counter += 1

if __name__ == "__main__":
    print ('''
    This script will produce of files containing the raw downloaded data organized
    by 100x100 km regions. Each region contains data for 100 10x10km sites.
    This process takes a while and will frequently fail. If and when it does, the
    process can be resumed where it broke by replacing the value for start_prefix
    with the last value printed out.''')
    raw_input('...')
    from sys import argv
    if len(argv) == 1:
        start_prefix = 0
    elif len(argv) == 2:
        start_prefix = argv[1]
    else:
        print 'Error: too many arguments'
        start_prefix = None
    if start_prefix.isdigit():
        start_prefix = int(start_prefix)
        download_files(PREFIX_FILENAME, TAXON_CODE, TARGET_DIRECTORY, start_prefix)

