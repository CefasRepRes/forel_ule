# -*- coding: utf-8 -*-
"""
Author: Lenka Fronkova
Date: 28/09/2021
"""

###############################################################################
"""A set of functions that will be called by the driver_main.py and 
   executed to map river plumes using Sentinel-3 as input data. Before you run
   these scripts, please download S3 data from EUMETSAT. You can use 'unzippingTar'
   or 'unzippingZip' function to iteratively unzip the downloaded files until you have folders
   with netcdf files and corresponding xml. Please refere to the folder structure in the GitHub
   for the functions to run seemlessly."""
###############################################################################   

"""This function unzips the tar files. If the downloaded file is corrupt,
it will print an error message

Arguments:
year = the processing year
monthsList = a list of months  in 2 digits format eg '01' or 'mm'
dataInputPath = a path to your downloaded S3 data in tar format
    """   
def unzippingTar(year, monthsList, dataInputPath):
    import tarfile
    import os

    
    
    for month in monthsList:
        #change working directory
        os.chdir(dataInputPath+"\\"+year+"\\"+month+"\\")
        #list files in the directory
        files =os.listdir()        
                
        for file in files:
            try:
                with tarfile.open(dataInputPath+"\\"+year+"\\"+month+"\\"+file) as tar:
                    tar.extractall()
                    tar.close()
                    print(month)
                    print(file)
            except tarfile.ReadError:
                print("File {} is corrupt".format(file))
        print("Unzipping was successfully completed for year: "+year+" and month:"+month)

###############################################################################
"""Unzip the '.zip' files when you use the  Sentinel downloader from 
https://gitlab.eumetsat.int/eumetlab/cross-cutting-tools/sentinel-downloader
which creates the format: year- month-day

Arguments:
pathData = a path to your downloaded S3 data in zip format
year = a string with the year of the format 'Y'YYY''
month =  a list of months  in 2 digits format eg '01' or 'mm'"""


def unzippingZip_sen_d(pathData, year, month):
    
    import calendar
    import os
    import zipfile
    import glob
    
    #create a list of days based on a month and year
    year_i = int(year)
    month_i = int(month)
    num_days_month = calendar.monthrange(year_i, month_i)[1]
    
    #loop and create the number of days
    days_month =[]
    for day in range(1, num_days_month+1):
        days_month.append(str(day))
        
    #change the string- fill in the zero before the single digit
    for i in range(9):
        days_month[i] = days_month[i].zfill(2)
        
    for d in days_month:
        
        files = glob.glob(pathData+year+"/"+month+"/"+d+"\\*.zip")
        
        #change directory back to the month where the zipped files will be extracted
        os.chdir(pathData+year+"/"+month+"/")

        
        for file in files:
            try:
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall()
                    print(month)
                    print(file)
            except zipfile.ReadError:
                    print("File {} is corrupt".format(file))        


##############################################################################    
"""This function calls the xml file and uses the gpt which allows batch processing
using SNAP functions. The function calls xmlGraph which subsets the image,
calculates Forel-Ule (FU Classification SNAP), reprojects and exports a 
geotiff. Currently this works with WGS 1984 projection. The xmlGraph needs 
changing if run on a different location than Liverpool Bay area of interst
marked in GitHub. Check line 61 in case the path length
changes. The xlmGraph is called with the inputs and outputs in the terminal (cmd)

Arguments:
path= path to S3 unzipped data containing xmls
outputPath= output path where you want to export the final goetiff
xmlGraph= path to the xmlGraph containing SNAP functions
year= processing year 'YYYY'
month= processing month 'mm' format
""" 
   
def ForelUleSnap(path, outputPath, xmlGraph, year, month):

    import subprocess
    import glob

    #############assign variables##############

    dataList = glob.glob(path+"/"+year+"/"+month+"/*.SEN3")
    dataList.sort()
    ##########################################
    
    for i in range(len(dataList)):


        print(str(i))
        inputData = dataList[i]+"/xfdumanifest.xml"
        
        date = dataList[i].split('\\')[1][16:24] #check in case the path changes
        print(date+" and index: "+str(i))
        
        inputData = inputData.replace("\\", "/")
        
        outputData = outputPath+"/"+month+"/fu_"+date+"_"+str(i)+".dim"
        
        #create cmd command
        command = "gpt "+xmlGraph+" -t "+outputData+" "+inputData
        print("Processing...")
        print(inputData)
        #run the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        print(stdout)
        #subprocess.call(command, shell=True)
        print("Successfully created FU.")


"""Clip the area using ESRI arcpy module from ArcGIS Pro and resample so the
rasters have the same number of columns and rows. Make sure this is run in your
cloned ArcGIS Pro environment. For the pathMask argument, please check the information in
the supplementary_data.txt


Arguments:
pathIn = data path to the exported geotif from ForelUleSnap
pathOut = data path out (please check READ_ME for the proposed structure)
year = processing year 'YYYY'
month = processing month 'mm'
pathMask = please refer to the READ_ME on GitHub
cellsize = output cell size, for S3 data we used 0.003 0.003
westound = the most westerly point
eastbound = the most easterly point
northbound = the most northly point
southbound = the most southerly point
for Liverpool Bay we used the following coordinates: -4.4 53 -2.6008 54.3" 
""" 

def clip( pathIn, pathOut,year, month, pathMask, cellsize, westbound, eastbound, northbound, southbound ):
    import arcpy
    from pathlib import Path
    import glob
    
    #get the input file paths with folder names
    dataList = glob.glob(pathIn+"/"+month+"/*.data")

    
    ###set environment
    arcpy.env.mask = pathMask
    arcpy.env.overwriteOutput = True
    arcpy.env.snapRaster = pathMask
    
    aoi = pathMask
    
    #create a range of dates
    for i in range(len(dataList)):
        data = dataList[i].replace("\\", "/")
        f = Path(data+"/FU.img")
        if f.is_file() == True:
            print("Processing for:")
            print(str(i))
            
            date = data.split(".")[0].split("_")[-2]
            original_number = dataList[i].split("\\")[1].split("_")[-1].split(".")[0]
            print("Date :"+date)
            print("Index :"+original_number)
            
            #####################resample#####################################
            arcpy.Resample_management(in_raster=data+"/FU.img", 
                                      out_raster=pathOut+"/"+month+"/fu_re_"+date+"_"+original_number+".tif", 
                                      cell_size=cellsize+" "+cellsize,#0.003 0.003", 
                                      resampling_type="NEAREST")
            
            
            print("Resampled")
        
            # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
            # The following inputs are layers or table views: "FU.img", "LB_aoi.tif"
            arcpy.Clip_management(in_raster=pathOut+"/"+month+"/fu_re_"+date+"_"+original_number+".tif",
                                  rectangle=westbound+" "+southbound+" "+eastbound+" "+northbound, #-4.4 53 -2.6008 54.3" 
                                  out_raster=pathOut+"/"+month+"/fu_clip_"+date+"_"+original_number+".tif", 
                                  in_template_dataset=aoi, 
                                  nodata_value="-9999", 
                                  clipping_geometry="NONE", 
                                  maintain_clipping_extent="MAINTAIN_EXTENT")
            print("Clipped finished")
            
            ###############delete the resampled data to clean the folder###########################
            arcpy.Delete_management(pathOut+"/"+month+"/fu_re_"+date+"_"+original_number+".tif")
                        
            
        else:
            print("This FU has not been computed:")
            print(date)

###############################################################################
"""Export numpy array as tif using an existing tif template. This function is used
to export processed arrays in other functions. You need to create a template as
described in please in the supplementary_data.txt

Arguments:
templateTif = a tiff tempalte (please check READ_ME for more info)
outputPath = data path out (please check READ_ME for the proposed structure)
outputRasterName = output taster name (without .tif extension) ,
arrayExport = array that you are exporting, 
na_val = nan value, normally we use numpy.nan for na_val
"""
def exportTif(templateTif, outputPath, outputRasterName, arrayExport, na_val):
    import gdal
    or_raster = gdal.Open(templateTif)       
    
    rows=or_raster.RasterYSize #length of Y (rows)
    cols=or_raster.RasterXSize #length of X (columns)
    geot=or_raster.GetGeoTransform()
    srs=or_raster.GetProjection()
    
    driver = gdal.GetDriverByName("GTiff")
    rasterOut = driver.Create(outputPath+outputRasterName+".tif", cols, rows, 1, gdal.GDT_Float32)
    
    
    rasterOut.SetGeoTransform(geot)
    rasterOut.SetProjection(srs)
    rasterOut.GetRasterBand(1).SetNoDataValue(na_val)
    
    rasterOut.GetRasterBand(1).WriteArray(arrayExport)
    rasterOut = None
    
    
##############################################################################

"""Clean coastal outliers that are most likely due to mud-flats or intertidal
area. Firstly we remove values <= 5 in forel-ule in the area of the 
interitdal mask. For more information how to create an intertidal mask, please check
the supplementary_data.txt. The same applies for the sea_mask, although this is used across
processing to align and snap rasters so they can stackedin the further steps.

Arguments:
intertidal_mask = an intertidal mask developed for Liverpool Bay (please check the information in
the supplementary_data.txt), 
sea_mask_Path = a sea mask developed for Liverpool Bay (please check the information in
the supplementary_data.txt), 
inputPath = path with the clipped and resampled rasters from 'clip' function, 
month = processing month in 'mm' format, 
year = processing year 'YYYY', 
outputPath = data path out (please check the
the supplementary_data.txt for the proposed structure), 
templateTif = a tiff tempalte (please check the information in
the supplementary_data.txt) which for 'exportTif' function
na_val = nan value, normally we use numpy.nan for na_val
"""
def coastal_clean_Forel_Ule(intertidal_mask, sea_mask_Path, inputPath, month, year, outputPath, templateTif, na_val):
    import numpy as np
    import rasterio
    import glob
    
    #open intertidal mask
    mask = rasterio.open(intertidal_mask)
    mask_ar = mask.read(1)
    
    #open sea mask    
    mask_sea = rasterio.open(sea_mask_Path)
    mask_sea = mask_sea.read(1)
    #turn 0 or land to np.nan, end up with 1= sea and na= land
    mask_sea = np.where(mask_sea==0, np.nan, mask_sea)
    
    
    ###########################################################################
    dataList = glob.glob(inputPath+"/"+month+"\\*.tif")
    
    for i in range(len(dataList)):
        
         date = dataList[i].split("\\")[1].split("_")[-2]
         original_number = dataList[i].split("\\")[1].split("_")[-1].split(".")[0]
         print("Date :"+date)
         print("Index :"+original_number)

         r = rasterio.open(dataList[i])
         r_array = r.read(1)
         
         #double check the number of rows and columns
         row = r_array.shape[0] 
         print("Row number: "+str(row))
         
         col = r_array.shape[1]
         print("Col number: "+str(col))
         
        

         #########remove values which are lower or equal to 5 in intertidal zones#######
         clean_ar = np.where((mask_ar ==1) & (r_array <=5), np.nan, r_array)
             
        #########clip by the sea mask####################################################
         clean_ar = np.where(mask_sea ==1, clean_ar, np.nan)
        
         ######turn 0 to nan#####
         clean_ar[clean_ar ==0.0] = np.nan
             

         exportTif(templateTif= templateTif, 
                      outputPath = outputPath+"/"+month+"/" , 
                      outputRasterName = "fu_"+date+"_"+original_number+"_clean_", 
                      arrayExport=clean_ar, 
                      na_val=na_val)
         print("Successfully exported.")
   
###############################################################################
"""Function to aggregate all the cleaned forel-ule data to monthly outputs as
a mean, max, min, standard deviation and counts the number of missing values per
pixel raster stack. It is important to have the same number of row and columns 
(resolution) of the rasters. Otherwise this funciton will not work. 'clip' 
function should make sure this happens.
Arguments:
    
month = processing month 'mm', 
year = processing year 'YYYY', 
inputPath = input data from 'coastal_clean_Forel_Ule' function, 
path_out = data path out (please check the information in the supplementary_data.txt for the proposed structure), 
templateTif = a tiff tempalte (please check the information in
the supplementary_data.txt)used for 'exportTif' function
na_val = nan value, normally we use numpy.nan for na_val ,
path_out_tif = data path out (please check the information in the supplementary_data.txt for the proposed structure)
"""

def ag(month, year, inputPath, path_out, templateTif,na_val,path_out_tif):
    import rasterio

    import numpy as np
    import matplotlib.pyplot as plt
    import glob
    import pandas as pd
    import gdal
        
    
    #create an empty list
    allArrays = []
    
    dataList = glob.glob(inputPath+"/"+month+"\\*.tif")
    
    for i in range(len(dataList)):
        data = rasterio.open(dataList[i])
        data_np= data.read(1)
        
        #convert 0 or -9999 to nans (if present)
        data_np_clean = np.where(data_np== 0, np.nan, data_np)
        data_np_clean = np.where(data_np_clean== -9999, np.nan, data_np_clean)
        
        row = data_np_clean.shape[0] 
        print("Row number: "+str(row))
        
        col = data_np_clean.shape[1]
        print("Col number: "+str(col))
                
        date = dataList[i].split("\\")[1].split("_")[1] #check if the path changes
        original_number = dataList[i].split("\\")[1].split("_")[2]
        print("Date :"+date)
        print("Index :"+original_number)
        
        #add the array to the list
        allArrays.append(data_np_clean)
        print("Appended")

    #stack a list of arrays into a 3D array
    stack = np.stack(allArrays, axis=2)
    
    #calculate mean
    stackMean = np.nanmean(stack, axis=2)
    plt.imshow(stackMean)
    plt.colorbar()
    plt.title("FU Mean for month:"+month+ " and year:"+year)
    plt.savefig(path_out+"FU_Mean_"+month+"_"+year+".png")
    plt.close()
    
    #calculate min
    stackMin = np.nanmin(stack, axis=2)
    plt.imshow(stackMin)
    plt.colorbar()
    plt.title("FU Minimum for month:"+month+ " and year:"+year)
    plt.savefig(path_out+"FU_Min"+month+"_"+year+".png")
    plt.close()
    
    #calculate max
    stackMax = np.nanmax(stack, axis=2)
    plt.imshow(stackMax)
    plt.colorbar()
    plt.title("FU Maximum for month:"+month+ " and year:"+year)
    plt.savefig(path_out+"FU_Max"+month+"_"+year+".png")
    plt.close()
    
    #calculate std
    stackStd = np.nanstd(stack, axis=2)
    plt.imshow(stackStd)
    plt.colorbar()
    plt.title("FU Standard deviation for month:"+month+ " and year:"+year)
    plt.savefig(path_out+"FU_STD_"+month+"_"+year+".png")
    plt.close()
    
    #calcuate count of nan in a stack
    stackVal = np.sum(np.isnan(stack),axis=2)
    plt.imshow(stackVal)
    plt.colorbar()
    plt.title("Count of missing values for month:"+month)
    plt.savefig(path_out+"FU_Count_missing_values_"+month+"_"+year+".png")
    plt.close()
    
    
    #################export tif knowing according to an input rastertemplate###


    arrays = [stackMean,stackMin, stackMax, stackStd, stackVal]
    names = ["FU_"+year+"_"+month+"_mean","FU_"+year+"_"+month+"_min", "FU_"+year+"_"+month+"_max","FU_"+year+"_"+month+"_std","FU_"+year+"_"+month+"_count_missing"]
    
    
    for ar, name in zip(arrays, names):
       
        exportTif(templateTif=templateTif, 
                  outputPath= path_out_tif, 
                  outputRasterName = name, 
                  arrayExport=ar, 
                  na_val=na_val)
        print("Exported:")
        print(name)


##########################INTERPOLATION########################################

"""Interpolation of missing values across the sea_mask (water pixels). Please
see the READ_ME for more information about how to create a sea_mask. IDW is used
for the interpolation from rasterio package with the chosen search_distance. Due
to the search distance, I extract the values that are water pixels using water
pixels. In other words, the interpolation creates values on land too so these need to 
be removed.

Arguments:
dataInputPath = data input from the 'ag' function, 
sea_mask =  a sea mask developed for Liverpool Bay (please check the information in the supplementary_data.txt) , 
outputPath = data path out (please check the information in the supplementary_data.txt), 
search_distance = integer,  3 pixels erere used in Liverpool Bay= 1km
year = processing year 'YYYY', 
month = processing month 'mm'
"""

def interpolation(dataInputPath, sea_mask, outputPath, search_distance, year, month, na_val):
    import rasterio
    from rasterio import fill
    import numpy as np
    
    r = rasterio.open(dataInputPath+"FU_"+year+"_"+month+"_mean.tif")
    r_array = r.read(1)
     
    #open sea mask    
    mask_sea = rasterio.open(sea_mask)
    mask_sea = mask_sea.read(1)
    #turn 0 or land to np.nan
    mask_sea = np.where(mask_sea==0, np.nan, mask_sea)
    
    #######################create a mask for the scence############################
        
    """mask : numpy ndarray or None
        A mask band indicating which pixels to interpolate. Pixels to
        interpolate into are indicated by the value 0. Values > 0
        indicate areas to use during interpolation. Must be same shape
        as image. If `None`, a mask will be diagnosed from the source
        data."""
    
    #create a mask to follow the above rule
    m = np.where((mask_sea ==1) & (np.isnan(r_array)), 0, mask_sea)
    
    #interpolate the pixels that have missing values by the ones that have 1s (search distance- ~ 1 km)
    interp = fill.fillnodata(r_array, mask =m, max_search_distance=search_distance, smoothing_iterations=0)
    
     #########clip by the sea mask####################################################
    interp = np.where(mask_sea ==1, interp, np.nan)
    interp = np.round(interp,0)
    
    
    exportTif(templateTif= dataInputPath+"FU_"+year+"_"+month+"_mean.tif", 
                      outputPath = outputPath+"ag_interpolated/" , 
                      outputRasterName = "FU_"+year+"_"+month+"_mean", 
                      arrayExport=interp, 
                      na_val=na_val)
    
    print("Exported")

#############################PLUME#############################################

"""Extract plume based on the values of forel-ule >= 10 and export the outputs
as tiff

Arguments:
dataInputPath = data input from the 'interpolation' function , 
outputPath = data path out (please check the information in the supplementary_data.txt for the proposed structure), 
year = a processing year 'YYYY', 
month = a processing month 'mm', 
ag  = 'Mean' #aggregation used 
na_val = nan values , normally use numpy.nan 

"""

def plumeMapping(dataInputPath, outputPath, year, month, ag, na_val):
    import rasterio
    import gdal
    import numpy as np
    
    print(ag)
    print(month)
    r = rasterio.open(dataInputPath+"FU_"+year+"_"+month+"_"+ag+".tif")
    r_array = r.read(1)
    
    plume = np.where(r_array>=10, np.nan, 1)
    
    
    #invert 1 and nan (the above doesn not account for land nans)
    plume = np.where(np.isnan(plume), 1, np.nan)
  
    
    exportTif(templateTif= dataInputPath+"FU_"+year+"_"+month+"_"+ag+".tif", 
                      outputPath = outputPath , 
                      outputRasterName = "FU_"+year+"_"+month+"_"+ag+"_plume", 
                      arrayExport=plume, 
                      na_val=na_val)
    
    print("Plume was Exported")






























      
