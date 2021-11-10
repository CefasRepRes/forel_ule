# Application of Forel-Ule to classify water in Liverpool Bay, UK

This repository contains functions and explanation on the methods of applying Forel-Ule method to classify water using Sentinel-3 optical satellite.


## Introduction

**ADD**

Classify the FU results in the classes 1-5, 6-9, 10-13, 14-17, 18-21 according to the accepted definitions in italics below. The indigo blue to greenish blue waters (FU colour classes 1-5) corresponds to waters with high light penetration. These waters often have low nutrient levels and low production of biomass. The colour is dominated by microscopic algae (phytoplankton). The greenish blue to bluish green (FU colour classes 6-9) correspond to waters with a colour still dominated by algae, but also increased dissolved organic matter and some sediment may be present and are typical for areas towards the open sea. The greenish waters (FU colour classes 10-13) correspond to coastal waters which usually display increased nutrient and phytoplankton levels, but also contain sediment and dissolved organic material. The greenish brown to brownish green waters (FU colour classes 14-17) correspond to waters with high nutrient and phytoplankton concentrations, but also increased sediment and dissolved organic matter and are typical for near-shore areas and tidal flats. Finally, the brownish green to cola brown waters (FU colour classes 18-21) correspond to waters with an extremely high concentration of humic acids, and are typical for rivers and estuaries (URL: http://www.citclops.eu/)"

## Methods

This repository contains scripts and functions to map river plumes using OLCI Sentinel-3 satellite data. There are two main scripts:
1. driver_main.py which calls the functions from 2. functions.py file. The majority of the functions used are open source based on numpy, rasterio
and gdal libraries. However, we also use the arcpy library (ArcGIS Pro, Python 3) for clipping and resampling purposes. The following is the step by step method conducted:

![forel_ule_method_github](https://user-images.githubusercontent.com/23084713/141150734-531c0ea1-3064-416d-9d47-2b83f80d677b.jpg)



1. 

2. 

3. 

4. 

6. 




## Applications


**1. ADD**



## forel_ule GitHub repository 

**driver_main.p** - the main driver that imports and run functions from functions.py

**functions.py** - all functions used for processing

**xmlGraph.xml** - a graph used in the batch processing using SNAP GPT functionality. It subset the scene, applies FU Classification, reprojects and exports the raster. The input is the downlaoded and unzipped S3 data containing pointing to the .xml. The graph could be run directly in the cmd terminal. The function ForelUleSnap calls the terminal and runs the graph looping thorugh all the data

**READ_ME.txt** - supplementary information on the data structure and auxiliary layers that were created specifically to run the analysis in the Liverpool Bay, UK


## Reference

Fronkova et al., 2021 - to add

Petus et al., 2019: https://pubmed.ncbi.nlm.nih.gov/31352278/

van der Woerd and Wernand, 2018: https://www.mdpi.com/2072-4292/10/2/180

van der Woerd and Wernand, 2015: https://pubmed.ncbi.nlm.nih.gov/26473859/

Wernand et al, 2013: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0063766&type=printable

Wernand, Hommerson, van der Woerd, 2012: https://os.copernicus.org/preprints/9/2817/2012/osd-9-2817-2012.pdf

Devlin et al., 2009: https://www.researchgate.net/publication/228107427_Estimating_the_diffuse_attenuation_coefficient_from_optically_active_constituents_in_UK_marine_waters

https://github.com/jobel-openscience/FUME

## Authors

Lenka Fronkova (lenka.fronkova@cefas.co.uk)


## Data

Sentinel-3 A, B data could be downloaded using the EMUMETSAT service though these links and dates:

| Date    |	Description | Link |
| ------------     |  ------------------ | ------------------ |
| 01/01/2017 - 29/11/2017     |     EUMETSAT Codarep web portal    | https://codarep.eumetsat.int/#/home |
| 04/07/2017 - 31/12/2020  |	  EUMETSAT Service Client- Data Centre*     | Authentication - EUMETSAT - EO Portal User Registration |
|   Data up until 1 year old    |	 EUMETSAT Coda web portal  | https://coda.eumetsat.int/ |

*only manual donwload

Possible websites for automatic download:
https://gitlab.eumetsat.int/eumetlab/cross-cutting-tools/sentinel-downloader
https://sentinelsat.readthedocs.io/en/v0.8/api.html

examples of the scripts will be added to the repository

## Licence

This source code is licensed under the Open Government Licence v3.0. To view this licence, visit www.nationalarchives.gov.uk/doc/open-government-licence/version/3 or write to the Information Policy Team, The National Archives, Kew, Richmond, Surrey, TW9 4DU.

The Open Government Licence (OGL) Version 3

Copyright (c) 2021 Centre for Environment Fisheries and Aquaculture Science

