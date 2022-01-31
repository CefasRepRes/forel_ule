################SUPPLEMENTARY MATERIAL ON THE SCRIPTS AND DATA#################

########################1. DATA STRUCTURE######################################
CREATE THE FOLLOWING DATA STRUCTURE IN ORDER TO BE COMPATABLE WITH THE SCRIPTS
(RECOMMENDED)

1.Create folders 'analysis'and 's3_data'

2. In the 'analysis', create the following subfolders:
'year' (e.g '2017') > 'coastal_cleaning' and 'fu_processing'

3. In the 'coastal_processing' create the following subfolder:
'months' substituted by '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'
and also 'ag', 'ag_interpolated' and 'ag_plume'

4. in 'fu_processing' create the following subfolders:
's3_fu_daily' and 's3_fu_daily_clipped'

5. In both 's3_fu_daily' and 's3_fu_daily_clipped' create the following subfolders:

'months' subsituted by'01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'
  
The following steps were conducted in ArcMap 10.5 software.

#####################2. AREA OF INTEREST MASK##################################
AN AREA OF INTEREST HAD TO BE CREATED FOR LIVERPOOL BAY. THIS TIFF SERVES FOR
SNAPPING THE RASTERS IN THE CLIPPING FUNCTION TO THE BOTTOM LEFT CORNER SO ALL
RASTERS LIGN-UP. 

Steps how it was created:
1. Creating the shapefile area of interest here:~\DP434\Working_Area\Data\Forel_Ule\analysis\aoi\LB_aoi.shp
2. Using Polygon to Raster tool to export LB_aoi.shp to LB_aoi.tif using 0.003
resolution

########################3. SEA MASK############################################
1. Create a fishnet using 0.003 resolution- set-up extent, environmneat setting 
such as resolution, snapping, extent etc accorindg to LB_aoi.tif

2. Create a new field 'sea_mask' in the fishnet

3. Use 'Select by spatial location' to intersect the coastline shapefile
wiht the full resolution (f) from here: https://www.ngdc.noaa.gov/mgg/shorelines/gshhs.html 
with the fishnet. This source of the coastline is one of the highest resolution coastlines publicly available.
However, please use the appropriate coastline fro your area of interest.

3. Create a new field in the sea_mask fishnet called 'class' ('short' type or in other words a short integer) . Use the 'Field calculator' and populate the 'class' field by 0 = land.
This will assign 0 to the fishnet grid squares which intersect the coast.

4. Reverse the selection order and use the field calculator to populate the 'class' column in the 'sea_mask'
by 1=water.

5. Use 'Polygon to raster' to convert the fishnet into a tif file called sea_mask.tif based on the 'class' field values.

#######################4.INTERTIDAL MASK######################################

1. Merge and dissolve coastal and transitional Water Framework Directive 
waterbodies shapefile
England: https://data.gov.uk/dataset/3a75ec5f-a361-475c-80e3-52d93bbc5dbe/wfd-transitional-and-coastal-waterbodies-cycle-2
Wales: http://lle.gov.wales/catalogue/item/WaterFrameworkDirectiveCoastalWaterbodiesCycle2?lang=en

2. Create a new field called 'int_mask' (type short) in the 'sea_mask' fishnet.

3. Use 'Select by spatial location' to intersect merged WFD waterbodies with the fishnet
and use field calculator to populate the "inter_mask" with 1. This will flag the grids that intersect the fishnet as 1.

4. Reverse selection and use the field calculator to populate the 'inter_mask'
with 0.

5. Use 'Polygon to raster' tool to exort the intertidal_mask.tif using the 'inter_mask' field.

6. Expand the intertidal mask since it might not capture all the transitional
waters due to discrepancies in resolution between Sentinel 3 data and WFD waterbodies.
Run 'Expand' tool on the 'intertidal_mask.tif' with number of cells = 2.

7. This mask will be used to clean the coastal areas in the process.



intertidal_mask="~/DP434/Working_Area/Data/Forel_Ule/analysis/cleaning_working_area/WFD_mask_expand.tif", 
sea_mask_Path = "~/DP434/Working_Area/Data/Forel_Ule/analysis/cleaning_working_area/sea_mask_LB.tif",

