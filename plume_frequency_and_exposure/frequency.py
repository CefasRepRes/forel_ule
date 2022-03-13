# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 14:48:27 2022

@author: LF06
"""

import rasterio
#from rasterio.mask import mask
import numpy as np
import matplotlib.pyplot as plt
import glob
#import pandas as pd
#from pathlib import Path
import gdal
#import calendar
import seaborn as sns

##################function to export a tif######################################

'''export tif using a known template'''
def exportTif(templateTif, outputPath, outputRasterName, arrayExport, na_val):
    #import gadal
    or_raster = gdal.Open(templateTif)
    
    
    rows=or_raster.RasterYSize #length of Y (rows)
    cols=or_raster.RasterXSize #length of X (columns)
    geot=or_raster.GetGeoTransform()
    srs=or_raster.GetProjection()
    
    driver = gdal.GetDriverByName("GTiff")
    rasterOut = driver.Create(outputPath+outputRasterName, cols, rows, 1, gdal.GDT_Float32)
    
    
    rasterOut.SetGeoTransform(geot)
    rasterOut.SetProjection(srs)
    rasterOut.GetRasterBand(1).SetNoDataValue(na_val)
    
    rasterOut.GetRasterBand(1).WriteArray(arrayExport)
    rasterOut = None

##########################frequencies##########################################
#######revised frequencies according to primary (FU 14 – 21), 
#####secondary (FU 10 – 13), tertiary (FU 9 - 6) and Offshore (1 to 6)

def lb_freq(inputPath, year, outputPath, na_val):

    #create empty lists for waterbody classes
    dataList_primary = []
    dataList_secondary = []
    dataList_tertiary = []
    dataList_offshore = []
    
    
    print(year)
    
    #read the data
    data = glob.glob(inputPath+year+"/ag_interpolated/*mean.tif")
    
    #split the data according to the classes and flag them as 1 if they contain the specific forel-ule class
    for d in data:
        dd = rasterio.open(d)
        dd_ar= dd.read(1)
        primary = np.where(dd_ar >=14, 1, np.nan)
        secondary = np.where((dd_ar <14) & (dd_ar >=10), 1, np.nan)
        tertiary = np.where((dd_ar <10) & (dd_ar >=6), 1, np.nan)
        offshore = np.where(dd_ar <6, 1, np.nan)
        dataList_primary.append(primary)
        dataList_secondary.append(secondary)
        dataList_tertiary.append(tertiary)
        dataList_offshore.append(offshore)
        
    ########################primary########################################
    #create a raster stack
    rasterStack_p = np.stack(dataList_primary)
    
    #sum all the numbers (1s)
    stackSum_p = np.nansum(rasterStack_p, axis=0)
    
    #turn 0 to np.nan
    stackSum_p_clean = np.where(stackSum_p == 0, np.nan, stackSum_p)
    
    #change scale
    no = len(dataList_primary)
    print(str(no))

    stackSum_p_clean = stackSum_p_clean/no
    

    #export
    exportTif(templateTif = data[0], 
              outputPath = outputPath, 
              outputRasterName = "primary_freq_14_21_"+year+".tif", 
              arrayExport = stackSum_p_clean, 
              na_val = na_val)
    
    print("Primary class exported")
    
    #######################################################################
    ##########################secondary####################################
   
    #create a raster stack
    rasterStack_sec = np.stack(dataList_secondary)
   
    #sum all the numbers (1s)
    stackSum_sec = np.nansum(rasterStack_sec, axis=0)
   
    #turn 0 to np.nan
    stackSum_sec_clean = np.where(stackSum_sec == 0, np.nan, stackSum_sec)
    
    #change scale
    no = len(rasterStack_sec)

    stackSum_sec_clean = stackSum_sec_clean/no
   

    #export
    exportTif(templateTif = data[0], 
             outputPath = outputPath, 
             outputRasterName = "secondary_freq_13_10_"+year+".tif", 
             arrayExport = stackSum_sec_clean, 
             na_val = na_val)
    
    print("Secondary class exported")
        
        
    #######################################################################
    ###########################tertiary####################################
    
    #create a raster stack 
    rasterStack_ter = np.stack(dataList_tertiary)
    
    #sum all the numbers (1s)
    rasterStack_ter = np.nansum(rasterStack_ter, axis=0)
   
    #turn 0 to np.nan
    rasterStack_ter_clean = np.where(rasterStack_ter == 0, np.nan, rasterStack_ter)
    
    #change scale
    no = len(dataList_tertiary)

    rasterStack_ter_clean = rasterStack_ter_clean/no
   

    #export
    exportTif(templateTif = data[0], 
             outputPath = outputPath, 
             outputRasterName = "tertiary_freq_6_9_"+year+".tif", 
             arrayExport = rasterStack_ter_clean, 
             na_val = na_val)
    
    print("Tertiary class exported")
    
    #######################################################################
    ###########################offshore####################################
    
    #create a raster stack 
    rasterStack_offs = np.stack(dataList_offshore)
    
    #sum all the numbers (1s)
    rasterStack_offs = np.nansum(rasterStack_offs, axis=0)
   
    #turn 0 to np.nan
    rasterStack_ter_clean = np.where( rasterStack_offs == 0, np.nan,  rasterStack_offs)
    
    #change scale
    no = len(dataList_offshore)

    rasterStack_ter_clean = rasterStack_ter_clean/no
   

    #export
    exportTif(templateTif = data[0], 
             outputPath = outputPath, 
             outputRasterName = "offshore_freq_1_5_"+year+".tif", 
             arrayExport = rasterStack_ter_clean, 
             na_val = na_val)
    
    print("Offshore class exported")

    
##run the function
years = ["2017","2018", "2019", "2020", "2021"]

for year in years:
    lb_freq(inputPath="Z:/C8357_NCEA_Programme/Working_Area/C8357N Nearshore water quality/GIS_Data_Risk_Mapping/forel_ule_timeseries/", 
                year = year, 
                outputPath = "Z:/C8357_NCEA_Programme/Working_Area/C8357N Nearshore water quality/GIS_Data_Risk_Mapping/forel_ule_timeseries/class_frequencies/gbr_class/new_revised_06032022/", 
                na_val= np.nan)
    
    
    
    
    
    
    
    