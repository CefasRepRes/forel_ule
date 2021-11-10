# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 14:41:17 2021

@author: LF06
"""

#import all the functions from the 'functions' script
from functions import *

###############################STEP 1##########################################
###########unzipping of the tar files or zipped files##########################
###############################################################################

unzippingTar(year="2019",
             monthsList=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], 
             dataInputPath="E:\\plume_work\\liverpool_bay\\s3_data")



################################STEP 2#########################################
###########################FOREL-ULE CLASSIFICATION############################
###############################################################################
#run Forel-Ule classfication. Make sure you check the path still gives "date"
#in the desired format

months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
year = "2019"

##loop through the months
for month in months:
    ForelUleSnap(path = "E:/plume_work/liverpool_bay/s3_data",
                 outputPath= "E:/plume_work/liverpool_bay/analysis/"+year+"/fu_processing/s3_fu_daily",
                 xmlGraph = "E:/plume_work/liverpool_bay/analysis/scripts_lenka/plume_mapping/fuGraph.xml",
                 year= year,
                 month = month)
    

print("Forel-Ule was calculated.")

#############################STEP 3############################################
#####################RESAMPLING/CLIPPING/SNAPPING USING ARCPY##################
###############################################################################    

####this part needs to be run in the the ArcGIS Pro environmnet-import arcpy
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
year = "2019"

for month in months:
    clip( pathIn="E:/plume_work/liverpool_bay/analysis/"+year+"/fu_processing/s3_fu_daily", 
         pathOut="E:/plume_work/liverpool_bay/analysis/"+year+"/fu_processing/s3_fu_daily_clipped",
         year=year, 
         month=month, 
         pathMask="Z:/DP434/Working_Area/Data/Forel_Ule/analysis/aoi/LB_aoi.tif", 
         cellsize="0.003", 
         westbound="-4.4", 
         eastbound="-2.6008", 
         northbound="54.3", 
         southbound="53" )

print("Resampling and Clipping completed.")

##############################STEP 4###########################################
#####################CLEANING OUTLIERS#########################################
###############################################################################


months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
year = "2019"

    for month in months:
        coastal_clean_Forel_Ule(intertidal_mask="Z:/DP434/Working_Area/Data/Forel_Ule/analysis/cleaning_working_area/WFD_mask_expand.tif", 
                                sea_mask_Path = "Z:/DP434/Working_Area/Data/Forel_Ule/analysis/cleaning_working_area/sea_mask_LB.tif",
                                year=year,
                                inputPath="E:/plume_work/liverpool_bay/analysis/"+year+"/fu_processing/s3_fu_daily_clipped", 
                                month=month,                             
                                outputPath="E:/plume_work/liverpool_bay/analysis/"+year+"/coastal_cleaning",
                                templateTif="E:/plume_work/liverpool_bay/analysis/2020/fu_processing/s3_fu_daily_clipped/01/fu_clip_20200101_0.tif") #choose one of the forel-ule outputs as a template
    
    print("Costal cleaning was completed.")
    
    ############################STEP 5#############################################
    ########################MONTHLY AGGREGATION####################################
    
    months = [ "01","02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    year = "2017"
    
    for month in months:
        ag(month=month, 
           year=year, 
           inputPath="E:/plume_work/liverpool_bay/analysis/"+year+"/coastal_cleaning/", 
           path_out= "E:/plume_work/liverpool_bay/analysis/"+year+"/coastal_cleaning/figures_ag/",
           templateTif= "E:/plume_work/liverpool_bay/analysis/2020/fu_processing/s3_fu_daily_clipped/01/fu_clip_20200101_0.tif",
           path_out_tif="E:/plume_work/liverpool_bay/analysis/"+year+"/coastal_cleaning/ag/")
    
    print("Aggregation completed.")
    
    ############################STEP 6#############################################
    ###########################INTERPOLATION#######################################
    ###############################################################################
    
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    #months=["07"]
    year= "2017"
    
    for month in months:
        interpolation(dataInputPath="E:/plume_work/liverpool_bay/analysis/"+year+"/coastal_cleaning/ag/", 
                      sea_mask="Z:/DP434/Working_Area/Data/Forel_Ule/analysis/cleaning_working_area/sea_mask_LB.tif", 
                      outputPath= "E:/plume_work/liverpool_bay/analysis/"+year+"/coastal_cleaning/", 
                      search_distance=3, #july 2017=10
                      year=year,
                      month=month)
    
    print("Interpolation completed")
        
    #############################STEP 7############################################  
    #######################EXTRACT RIVER PLUME#####################################
    ###############################################################################
     
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    year = "2017"
    
    ag = ["mean"]
    
    for g in ag:
        for month in months:
             plumeMapping(dataInputPath="E:/plume_work/liverpool_bay/analysis/"+year+"/coastal_cleaning/ag_interpolated/",  
                          outputPath= "E:/plume_work/liverpool_bay/analysis/"+year+"/coastal_cleaning/ag_interpolated_plume/", 
                          year=year,
                          month=month,
                          ag=g) 
             
    print("Aggregation completed.")
    
    ################################################################################
    
    ag = ["mean"]
    
    for g in ag:
        for month in months:
              plumeMapping(dataInputPath="Z:/DP434/Working_Area/Data/Forel_Ule/forel_ule_timeseries/"+year+"/ag_interpolated/",  
                          outputPath= "Z:/DP434/Working_Area/Data/Forel_Ule/forel_ule_timeseries/"+year+"/ag_interpolated_plume/", 
                          year=year,
                          month=month,
                          ag=g)
    
    print("Plume was extracted")






