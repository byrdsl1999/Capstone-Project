# The British Isles Flowering Plant Resource

+ [Overview](#sepsis)
+ [How this app was created](#creation)
+ [How can I do this myself?](#howto)

## <a name="overview"></a>Overview

This web is targeted towards land managers and conservationists. It has two related functions. For land managers, it predicts the species which are potential invasive species to the particular area of land they are concerned about.  For conservationists who are interested in remediation of threatened or protected species, the app will recommend regions which are most suitable for the species they are concerned with.


## <a name="creation"></a>How This App Was Created

### Data Collection

The data was collected from the [National Biological Networks](https://data.nbn.org.uk/) database. This database is an aggregation of biodiversity records and surveys. Through the database one can access records of the distribution and location of thousands of species going back hundreds of years in the British Isles. This represents perhaps the region with the most thoroghly cataloged record of biodiversity in the world. 

For this project I collected the publically available records of flowering plant species lists at a 10km resolution. The database has broken down the entirety of the British Isles into 10km x 10km squares and provides lists of the taxa from a particular taxanomic group(e.g. birds, flowering plants, butterflies) present in that particular region. I created a program which would request, download and collect this data for the entire region.

Once data was collected, further processing was done to distill the data to the essential parts for our analysis. Additionally, taxa only present in one or two regions were removed. Many of these 'taxa' represent data entry errors, or exceptional cases(e.g. arboretum or botanical specimens) which are unlikely to be of practical significance. Regions with fewer than 100 taxa were removed, as these sites tended to be small islands which were unlikely to be thoroughly surveyed, or likely data entry errors(e.g. a couple of plants were recorded at sites deep in the Atlantic Ocean).

### The Models

The models ultimately used were created using graphlab's ranking factorization recommender. Models were created using both trimmed and untrimmed data, and also binary and survey proportional data. After examining the models it appeared that a timmed binary model created the best recommendations for endangered species whereas the trimmed proportional data provided the best invasive species recommendations.

I also considered item-item similarity recommenders and factorization recommenders. All of these models were tuned before comparisons. 

### The App

The app uses flask as a wrapper to allow access to the recommender. It also flags taxa from various lists, and links to maps and wikipedia pages for the taxa genuses.

## <a name="howto"></a>How can I run this?

### The Easy Way:

The quickest way to see the project is to run the app.py program in python. In bash, navigate to the project directory and run the following command:

```bash
python app/app.py
```


Now open a browset and paste the following into the nav bar.

```url
0.0.0.0:8080
```

### The Harder Way:
#### Data Pipeline:
First, download the data with the program 'data_fetching.py'. This will download records of all of a specified taxanomic group in the British Isles. By default this is the flowering plants, but other groups can be set by changing global variables(I'm excited to try it with birds). These records will be stored in a 'data' directory, which can be quite large. If not all of the data is downloaded in one pass, the download can be resumed midway through by following the program instructions.

```bash
ipython data_fetching.py
```

Second, run the program 'data_preprocessing.py' to process the data. There are a couple of options, but the defaults work best. This will colate the data and preserve it in a s-frame file in the data directory.

```bash
ipython data_preprocessing.py
```

#### Model Creation
Models can be created by using either the 'binary_recommender_creator.py' or the 'proportional_recommender_creator.py'. Which one you should use depends on which type of data you created using 'data_preprocessing.py'. 

```bash
ipython binary_recommender_creator.py
```
or

```bash
ipython proportional_recommender_creator.py
```

This should produce a tuned NMF collaborative filtering model. Different models can also be created by adjusting the input data with the global variables in 'data_preprocessing.py'. 


#### Webapp
Once the model is created, the 'model' directory can be moved into the 'app' directory. If you run the 'app.py' program in the 'model' directory, you can now access the model through a webapp in a web browser at the url address 

```bash
0.0.0.0:8080
```
