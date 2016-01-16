# The British Isles Plant Utility


## OVERVIEW


This web is targeted towards land managers and conservationists. It has two related functions. For land managers, it predicts the species which are potential invasive species to the particular area of land they are concerned about.  For conservationists who are interested in remediation of threatened or protected species, the app will recommend regions which are most suitable for the species they are concerned with.

## Principle 

## HOW THIS APP WAS CREATED

### Data Collection

The data was collected from the National Biological Networks database. This database is an aggregation of biodiversity records and surveys. Through the database one can access records of the distribution and location of thousands of species going back hundreds of years in the British Isles. This represents perhaps the region with the most thoroghly cataloged record of biodiversity in the world. 

For this project I collected the publically available records of flowering plant species lists at a 10km resolution. The database has broken down the entirety of the British Isles into 10km x 10km squares and provides lists of the taxa from a particular taxanomic group(eg birds, flowering plants, butterflies) present in that particular region. I created a program which would request, download and collect this data for the entire region.

Once data was collected, further processing was done to distill the data to the essential parts for our analysis. Additionally, taxa only present in one or two regions were removed. Many of these 'taxa' represent data entry errors, or exceptional cases(e.g. arboretum or botanical specimens) which are unlikely to be of practical significance. Regions with fewer than 100 taxa were removed, as these sites tended to be small islands which were unlikely to be thoroughly surveyed, or likely data entry errors.

### The Model

### The App

## CODE: How can I recreate this?

### Data Pipeline

### Model Creation

### Webapp


