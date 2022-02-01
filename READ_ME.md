# Application of Forel-Ule to classify water in Liverpool Bay, UK

This repository contains functions and explanation on the methods of applying Forel-Ule (FU) method to classify ocean colour satellite product using OLCI Sentinel-3 .


## Introduction

The ocean colour can be used to provide information on the bio-physico-chemical processes of the water. The optically active constituents of the water determine its inherent optical properties (IOPs), and as such, the water’s ability to absorb, transmit, reflect or attenuate the sunlight. Historically, the ocean colour has been used to classify water into waterbodies based on the FU scale comparator. The FU scale consists of 21 values, ranging from indigo blue to brown. The colour of the water serves as a proxy of the water processes within. The indigo blue to greenish blue waters (FU colour classes 1-5) corresponds to waters with high light penetration. These waters often have low nutrient levels and low production of biomass. The colour is dominated by microscopic algae (phytoplankton). The greenish blue to bluish green (FU colour classes 6-9) correspond to waters with a colour still dominated by algae, but also increased dissolved organic matter and some sediment may be present and are typical for areas towards the open sea. The greenish waters (FU colour classes 10-13) correspond to coastal waters which usually display increased nutrient and phytoplankton levels, but also contain sediment and dissolved organic material. The greenish brown to brownish green waters (FU colour classes 14-17) correspond to waters with high nutrient and phytoplankton concentrations, but also increased sediment and dissolved organic matter and are typical for near-shore areas and tidal flats. Finally, the brownish green to cola brown waters (FU colour classes 18-21) correspond to waters with an extremely high concentration of humic acids, and are typical for rivers and estuaries (For more information please see URL: http://www.citclops.eu/)"

## Methods

This repository contains scripts and functions to map river plumes using OLCI Sentinel-3 satellite data. There are two main scripts:
**driver_main.py** which calls the functions from the **functions.py file**. The majority of the functions used are open source, including numpy, rasterio
and gdal libraries. However, we also use the ArcGIS arcpy library (Python 3) for clipping and resampling purposes. The following is the step by step method:

![forel_ule_method_github](https://user-images.githubusercontent.com/23084713/149539666-53bc368c-3497-4ea8-bb26-529b219a1e4a.jpg)



1. Download Sentinel- 3 data, depending on the time period that is needed. Please refer to the data section below.

2. Calculating the FU scale using Sentinel-3 data based on the algorithm developed in the European Citclops project, which is a part of the European Space Agency SNAP software. This was run in an automated Python 3 script using a Graph Processing Framework/Tool (https://senbox.atlassian.net/wiki/spaces/SNAP/pages/70503590/Creating+a+GPF+Graph)

3. The FU rasters were clipped and and resampled to a common grid (0.003x0.003 resolution) using arcpy library from ArcGIS (Python 3).

4. Coastal outliers were cleaned by removing values FU<=5, as these values correspond to open waters with a high light penetration that is not present in the coastal waters. 
This was performed over a mask created from Coastal and Transitional Water Framework Directive Waterbodies that can be found here: https://data.gov.uk/dataset/37709cf6-054f-40d9-be4e-ff2846c73743/water-framework-directive-wfd-river-waterbodies-cycle-2 . The erroneous values present in the coastal regions most likely result from the tidal changes
and the presence of sand banks.

5. Since the daily data contain gaps due to the presence of cloud cover, the daily FU outputs were aggregated to monthly composites using avearge from the Python numpy library.

6. Dispite the monthly aggregation and the aim to conserve as much of the actual data as possible, the monthly aggregated products still contained some gaps. As such, the inverse distance interpolation from rasterio.fill library was used with ~1km search distance to fill in any gaps.

7. Fu values >=10 were extracted and flagged as 1, which signified the final river plume extent.


## The 'forel_ule' GitHub repository files: 

[driver_main.py](https://github.com/CefasRepRes/forel_ule/blob/main/driver_main.py) - the main driver that imports and run functions from functions.py 

[functions.py](https://github.com/CefasRepRes/forel_ule/blob/main/functions.py) - all functions used for processing

[xmlGraph.xml](https://github.com/CefasRepRes/forel_ule/blob/main/fuGraph.xml) - a graph used in the batch processing using SNAP GPT functionality. It subset the scene, applies FU Classification, reprojects and exports the raster. The input is the downlaoded and unzipped S3 data containing pointing to the .xml. The graph could be run directly in the cmd terminal. The function ForelUleSnap calls the terminal and runs the graph looping thorugh all the data

[supplementary_data.txt](https://github.com/CefasRepRes/forel_ule/blob/main/supplementary_data.txt) - supplementary information on the data structure and auxiliary layers that were created specifically to run the analysis in the Liverpool Bay, UK


## Reference

Fronkova et al., 2022 (in prep)

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

Sentinel-3 A, B data could be downloaded using the EMUMETSAT service for the specific time period. Please note that all of the options below require and online registration:

| Date    |	Description | Link |
| ------------     |  ------------------ | ------------------ |
| 01/01/2017 - 29/11/2017     |     EUMETSAT Codarep web portal    | https://codarep.eumetsat.int/#/home |
| 04/07/2017 - 31/12/2020  |	  EUMETSAT Service Client- Data Centre*     | Authentication - EUMETSAT - EO Portal User Registration |
|   Data up until 1 year old    |	 EUMETSAT Coda web portal  | https://coda.eumetsat.int/ |

*only manual donwload from the EUMETSAT Service Client Data Centre.

Possible websites for automatic download:
https://gitlab.eumetsat.int/eumetlab/cross-cutting-tools/sentinel-downloader
https://sentinelsat.readthedocs.io/en/v0.8/api.html

examples of the scripts will be added to the repository

## Licence

This source code is licensed under the Open Government Licence v3.0. To view this licence, visit www.nationalarchives.gov.uk/doc/open-government-licence/version/3 or write to the Information Policy Team, The National Archives, Kew, Richmond, Surrey, TW9 4DU.

The Open Government Licence (OGL) Version 3

Copyright (c) 2022 Centre for Environment Fisheries and Aquaculture Science

