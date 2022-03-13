# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:47:47 2022

@author: LF06
"""

import rasterio
import gdal
import numpy as np
import glob
import matplotlib.pyplot as plt

###add a loop for primary, secondary, tertiary and offshore
##add an export function

###########a function to reclassify frequency into 5 categories################
'''reclassifying raster'''
def freq_reclassify(freq_array):
    ######################classify water pixels by frequency#######################
    #0-0.2	= 1
    #>0.2-0.4 = 2
    #>0.4-0.6 = 3
    #>0.6 - 0.8	= 4
    #>0.8 - 1 = 5
    
    #reclassify
    reclass_fre = np.where(freq_array > 0.8, 5, freq_array)
    reclass_fre = np.where((reclass_fre <= 0.8) & (reclass_fre > 0.6), 4, reclass_fre)
    reclass_fre = np.where((reclass_fre <=0.6) & (reclass_fre >0.4), 3, reclass_fre)
    reclass_fre = np.where((reclass_fre <=0.4) & (reclass_fre >0.2), 2, reclass_fre)
    reclass_fre = np.where(reclass_fre <=0.2, 1, reclass_fre)
    
    #plt.imshow(reclass_fre)
    #plt.colorbar()
    
    return(reclass_fre)

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
 
#define ears and path variables 
years = ["2017", "2018", "2019", "2020", "2021"]
inputPath = "Z:/C8357_NCEA_Programme/Working_Area/C8357N Nearshore water quality/GIS_Data_Risk_Mapping/forel_ule_timeseries/class_frequencies/gbr_class/new_revised_06032022/"
outputPath = "Z:/C8357_NCEA_Programme/Working_Area/C8357N Nearshore water quality/GIS_Data_Risk_Mapping/forel_ule_timeseries/plume_risk/lb_classification/"


##############################################################################
################calculate the risk plume#######################################
###############################################################################

###########################primary#############################################

p_data = []

#get a list of the raster path
for year in years:
    d = inputPath+"primary_freq_14_21_"+year+".tif"
    p_data.append(d)
    
#read the data as a numpy array
for d in p_data:
    #read the data
    dd = rasterio.open(d)
    d_ar = dd.read(1)
    
    name = d.split("/")[9].split(".")[0]
    
    #classify frequency
    d_ar_clas = freq_reclassify(d_ar)
    
    ####################mulitply by the waterbody type class#######################
    #primary	4
    
    #multiply by the magnitude of the waterbody type
    reclass_fre_p = d_ar_clas *4
    
    #export raster
    exportTif(templateTif = inputPath+"primary_freq_14_21_"+year+".tif", 
              outputPath = outputPath,
              outputRasterName = name+"_risk_score.tif",
              arrayExport = reclass_fre_p, 
              na_val = np.nan)
    
    print("Primary: "+name+"_risk_score was exported.")


####################secondary#################################################
p_data = []

for year in years:
    d = inputPath+"secondary_freq_13_10_"+year+".tif"
    p_data.append(d)
    
    
for d in p_data:
    #read the data
    dd = rasterio.open(d)
    d_ar = dd.read(1)
    
    name = d.split("/")[9].split(".")[0]
    
    #classify frequency
    d_ar_clas = freq_reclassify(d_ar)
    
    ####################mulitply by the waterbody type class#######################
    #secondary	3
    
    #multiply by the magnitude of the waterbody type
    reclass_fre_p = d_ar_clas *3
    
    #export raster
    exportTif(templateTif = inputPath+"primary_freq_14_21_"+year+".tif", 
              outputPath = outputPath, 
              outputRasterName = name+"_risk_score.tif", 
              arrayExport = reclass_fre_p, 
              na_val = np.nan)
    
    print("Secondary: "+name+"_risk_score was exported.")

############################tertiary###########################################
p_data = []

for year in years:
    d = inputPath+"tertiary_freq_6_9_"+year+".tif"
    p_data.append(d)
    
    
for d in p_data:
    #read the data
    dd = rasterio.open(d)
    d_ar = dd.read(1)
    
    name = d.split("/")[9].split(".")[0]
    
    #classify frequency
    d_ar_clas = freq_reclassify(d_ar)
    
    ####################mulitply by the waterbody type class#######################
    #tertiary	2
    
    #multiply by the magnitude of the waterbody type (not necessary but just shown for the conecpt/justification)
    reclass_fre_p = d_ar_clas *2
    
    #export raster
    exportTif(templateTif = inputPath+"primary_freq_14_21_"+year+".tif", 
              outputPath = outputPath, 
              outputRasterName = name+"_risk_score.tif", 
              arrayExport = reclass_fre_p, 
              na_val = np.nan)
    
    print("Tertiary: "+name+"_risk_score was exported.")

############################offshore###########################################
p_data = []

for year in years:
    d = inputPath+"offshore_freq_1_5_"+year+".tif"
    p_data.append(d)
    
    
for d in p_data:
    #read the data
    dd = rasterio.open(d)
    d_ar = dd.read(1)
    
    name = d.split("/")[9].split(".")[0]
    
    #classify frequency
    d_ar_clas = freq_reclassify(d_ar)
    
    ####################mulitply by the waterbody type class#######################
    #offshore 1
    
    #multiply by the magnitude of the waterbody type (not necessary but just shown for the conecpt/justification)
    reclass_fre_p = d_ar_clas *1
    
    #export raster
    exportTif(templateTif = inputPath+"primary_freq_14_21_"+year+".tif", 
              outputPath = outputPath, 
              outputRasterName = name+"_risk_score.tif", 
              arrayExport = reclass_fre_p, 
              na_val = np.nan)
    
    print("Offshore: "+name+"_risk_score was exported.")

##############################################################################
###################original GBR classes from Petus et al. 2019################
##############################################################################
years = ["2017", "2018", "2019", "2020", "2021"]
inputPath = "Z:/C8357_NCEA_Programme/Working_Area/C8357N Nearshore water quality/GIS_Data_Risk_Mapping/forel_ule_timeseries/class_frequencies/gbr_class/original/"
outputPath = "Z:/C8357_NCEA_Programme/Working_Area/C8357N Nearshore water quality/GIS_Data_Risk_Mapping/forel_ule_timeseries/plume_risk/lb_original_gbr_classes/"


###########################primary#############################################

p_data = []

#get a list of the raster path
for year in years:
    d = inputPath+"primary_freq_10_21_"+year+".tif"
    p_data.append(d)
    
#read the data as a numpy array
for d in p_data:
    #read the data
    dd = rasterio.open(d)
    d_ar = dd.read(1)
    
    name = d.split("/")[9].split(".")[0]
    
    #classify frequency
    d_ar_clas = freq_reclassify(d_ar)
    
    ####################mulitply by the waterbody type class#######################
    #primary	4
    
    #multiply by the magnitude of the waterbody type
    reclass_fre_p = d_ar_clas *4
    
    #export raster
    exportTif(templateTif = inputPath+"primary_freq_10_21_"+year+".tif", 
              outputPath = outputPath,
              outputRasterName = name+"_risk_score.tif",
              arrayExport = reclass_fre_p, 
              na_val = np.nan)
    
    print("Primary: "+name+"_risk_score was exported.")


####################secondary#################################################
p_data = []

for year in years:
    d = inputPath+"secondary_freq_6_9_"+year+".tif"
    p_data.append(d)
    
    
for d in p_data:
    #read the data
    dd = rasterio.open(d)
    d_ar = dd.read(1)
    
    name = d.split("/")[9].split(".")[0]
    
    #classify frequency
    d_ar_clas = freq_reclassify(d_ar)
    
    ####################mulitply by the waterbody type class#######################
    #secondary	3
    
    #multiply by the magnitude of the waterbody type
    reclass_fre_p = d_ar_clas *3
    
    #export raster
    exportTif(templateTif = inputPath+"primary_freq_10_21_"+year+".tif", 
              outputPath = outputPath, 
              outputRasterName = name+"_risk_score.tif", 
              arrayExport = reclass_fre_p, 
              na_val = np.nan)
    
    print("Secondary: "+name+"_risk_score was exported.")

############################tertiary###########################################
p_data = []

for year in years:
    d = inputPath+"tertiary_freq_4_5_"+year+".tif"
    p_data.append(d)
    
    
for d in p_data:
    #read the data
    dd = rasterio.open(d)
    d_ar = dd.read(1)
    
    name = d.split("/")[9].split(".")[0]
    
    #classify frequency
    d_ar_clas = freq_reclassify(d_ar)
    
    ####################mulitply by the waterbody type class#######################
    #tertiary	2
    
    #multiply by the magnitude of the waterbody type (not necessary but just shown for the conecpt/justification)
    reclass_fre_p = d_ar_clas *2
    
    #export raster
    exportTif(templateTif = inputPath+"primary_freq_10_21_"+year+".tif", 
              outputPath = outputPath, 
              outputRasterName = name+"_risk_score.tif", 
              arrayExport = reclass_fre_p, 
              na_val = np.nan)
    
    print("Tertiary: "+name+"_risk_score was exported.")

############################marine###########################################
p_data = []

for year in years:
    d = inputPath+"marine_freq_1_3_"+year+".tif"
    p_data.append(d)
    
    
for d in p_data:
    #read the data
    dd = rasterio.open(d)
    d_ar = dd.read(1)
    
    name = d.split("/")[9].split(".")[0]
    
    #classify frequency
    d_ar_clas = freq_reclassify(d_ar)
    
    ####################mulitply by the waterbody type class#######################
    #offshore 1
    
    #multiply by the magnitude of the waterbody type (not necessary but just shown for the conecpt/justification)
    reclass_fre_p = d_ar_clas *1
    
    #export raster
    exportTif(templateTif = inputPath+"primary_freq_10_21_"+year+".tif", 
              outputPath = outputPath, 
              outputRasterName = name+"_risk_score.tif", 
              arrayExport = reclass_fre_p, 
              na_val = np.nan)
    
    print("Marine: "+name+"_risk_score was exported.")

###############################################################################
#################create annual scores together#################################
###############################################################################

riskPlumePath =  "Z:/C8357_NCEA_Programme/Working_Area/C8357N Nearshore water quality/GIS_Data_Risk_Mapping/forel_ule_timeseries/plume_risk/lb_classification/"
##annual

for year in years:
    print(year)
    #read data
    p_data = []
    d = rasterio.open(riskPlumePath+"primary_freq_14_21_"+year+"_risk_score.tif")
    d_ar = d.read(1)
    p_data.append(d_ar)
    d = rasterio.open(riskPlumePath+"secondary_freq_13_10_"+year+"_risk_score.tif")
    d_ar = d.read(1)
    p_data.append(d_ar)
    d = rasterio.open(riskPlumePath+"tertiary_freq_6_9_"+year+"_risk_score.tif")
    d_ar = d.read(1)
    p_data.append(d_ar)
    d = rasterio.open(riskPlumePath+"offshore_freq_1_5_"+year+"_risk_score.tif")
    d_ar = d.read(1)
    p_data.append(d_ar)
    
    
    

    #create a raster stack
    rasterS = np.dstack(p_data)
    
    #sum all the numbers (1s)
    stackSum= np.nansum(rasterS, axis=2)
    
   #np.unique(stackSum[~np.isnan(stackSum)])
    
    #turn 0 to nan
    stackSum= np.where(stackSum == 0, np.nan, stackSum)
    
    #export raster
    exportTif(templateTif = riskPlumePath+"primary_freq_14_21_"+year+"_risk_score.tif", 
              outputPath = riskPlumePath+"/annual_sum_all_wb/", 
              outputRasterName = "plume_risk_score_"+year+".tif", 
              arrayExport = stackSum, 
              na_val = np.nan)
    
    
    print("River plume risk score exported for: "+year)
    
    
    #rescale
    r_min = np.nanmin(stackSum)
    r_max = np.nanmax(stackSum)
    
    stackSum_rescale = (stackSum - r_min) / (r_max - r_min)
    
    
    
    #plt.imshow(stackSum_rescale)
    #plt.colorbar()
    
    #export raster
    exportTif(templateTif = riskPlumePath+"primary_freq_14_21_"+year+"_risk_score.tif", 
              outputPath = riskPlumePath+"/annual_sum_all_wb/", 
              outputRasterName = "plume_risk_score_"+year+"_rescaled.tif", 
              arrayExport = stackSum_rescale, 
              na_val = np.nan)
    print("Rescaled river plume risk score exported for: "+year)

###########################climatology taking all wb##########################

#read all the data
data_all = glob.glob(riskPlumePath+"*.tif")
data_all = data_all[5:]

data_clim = []

for year in years:
    print(year)

    d = rasterio.open(riskPlumePath+"primary_freq_14_21_"+year+"_risk_score.tif")
    d_ar = d.read(1)
    p_data.append(d_ar)
    d = rasterio.open(riskPlumePath+"secondary_freq_13_10_"+year+"_risk_score.tif")
    d_ar = d.read(1)
    p_data.append(d_ar)
    d = rasterio.open(riskPlumePath+"tertiary_freq_6_9_"+year+"_risk_score.tif")
    d_ar = d.read(1)
    p_data.append(d_ar)
    d = rasterio.open(riskPlumePath+"offshore_freq_1_5_"+year+"_risk_score.tif")
    d_ar = d.read(1)
    p_data.append(d_ar)

#read data as numpy array
for i in data_all:
    d = rasterio.open(i)
    d_ar = d.read(1)
    data_clim.append(d_ar)
    
#create a raster stack
rasterS = np.dstack(data_clim)
 
#sum all the numbers (1s)
stackSum= np.nansum(rasterS, axis=2)
 
#np.unique(stackSum[~np.isnan(stackSum)])
 
#turn 0 to nan
stackSum= np.where(stackSum == 0, np.nan, stackSum)
 
#export raster
exportTif(templateTif = riskPlumePath+"primary_freq_14_21_"+year+"_risk_score.tif", 
       outputPath = riskPlumePath+"climatology_sum/", 
       outputRasterName = "plume_risk_score_2017_2021_sum_without_offshore_v2.tif", 
       arrayExport = stackSum, 
       na_val = np.nan)
 
 
print("Climatology river plume risk score exported.")
 
 
#rescale
r_min = np.nanmin(stackSum)
r_max = np.nanmax(stackSum)
 
stackSum_rescale = (stackSum - r_min) / (r_max - r_min)
 
#plt.imshow(stackSum_rescale)
#plt.colorbar()
 
#export raster
exportTif(templateTif = riskPlumePath+"primary_freq_14_21_"+year+"_risk_score.tif", 
       outputPath = riskPlumePath+"climatology_sum/", 
       outputRasterName = "plume_risk_score_2017_2021_sum_rescaled_witout_offshore.tif", 
       arrayExport = stackSum_rescale, 
       na_val = np.nan)

print("Climatology rescaled river plume risk score exported for")

############climatology per water type#########################################
#read all the data

data_primary = []
data_secondary = []
data_tertiary = []
data_offshore = []

##############################################################################
for year in years:
    print(year)
    p = rasterio.open(riskPlumePath+"primary_freq_14_21_"+year+"_risk_score.tif")
    p_ar = p.read(1)
    data_primary.append(p_ar)
    s = rasterio.open(riskPlumePath+"secondary_freq_13_10_"+year+"_risk_score.tif")
    s_ar = s.read(1)
    data_secondary.append(s_ar)
    t = rasterio.open(riskPlumePath+"tertiary_freq_6_9_"+year+"_risk_score.tif")
    t_ar = t.read(1)
    data_tertiary .append(t_ar)
    of = rasterio.open(riskPlumePath+"offshore_freq_1_5_"+year+"_risk_score.tif")
    of_ar = of.read(1)
    data_offshore.append(of_ar)

    



###########################waterbody##################################


data_clim = data_secondary
wb = "secondary"

#################primary######################################################    
#create a raster stack
rasterS = np.dstack(data_clim)
 
#sum all the numbers (1s)
stackSum= np.nansum(rasterS, axis=2)
 
#np.unique(stackSum[~np.isnan(stackSum)])
 
#turn 0 to nan
stackSum= np.where(stackSum == 0, np.nan, stackSum)
 
#export raster
exportTif(templateTif = riskPlumePath+"primary_freq_14_21_"+year+"_risk_score.tif", 
       outputPath = riskPlumePath+"climatology_sum/", 
       outputRasterName = wb+"_plume_risk_score_2017_2021_sum.tif", 
       arrayExport = stackSum, 
       na_val = np.nan)
 
 
print("Climatology river plume risk score exported for: "+wb)
 

#####################get all the summed arrays and rescale based on the min and max
#####################from the whole series


off = rasterio.open(riskPlumePath+"climatology_sum/offshore_plume_risk_score_2017_2021_sum.tif")
off = of.read(1)

p  = rasterio.open(riskPlumePath+"climatology_sum/primary_plume_risk_score_2017_2021_sum.tif")
p = p.read(1)

s= rasterio.open(riskPlumePath+"climatology_sum/secondary_plume_risk_score_2017_2021_sum.tif")
s = s.read(1)

t = rasterio.open(riskPlumePath+"climatology_sum/tertiary_plume_risk_score_2017_2021_sum.tif")
t = t.read(1)


dstack = np.dstack([off,p,s, t])

 
#rescale
r_min = np.nanmin(dstack)
r_max = np.nanmax(dstack)

#define array
array = t
wb = "tertiary" 
stackSum_rescale = (array - r_min) / (r_max - r_min)
 
 
#plt.imshow(stackSum_rescale)
#plt.colorbar()
 
#export raster
exportTif(templateTif = riskPlumePath+"primary_freq_14_21_"+year+"_risk_score.tif", 
       outputPath = riskPlumePath+"climatology_sum/", 
       outputRasterName = wb+"_plume_risk_score_2017_2021_sum_rescaled_v2.tif", 
       arrayExport = stackSum_rescale, 
       na_val = np.nan)

print("Climatology rescaled river plume risk score exported for: "+wb)


#############climatology taking all the years##################################
riskPlumePath = "Z:/C8357_NCEA_Programme/Working_Area/C8357N Nearshore water quality/GIS_Data_Risk_Mapping/forel_ule_timeseries/plume_risk/lb_classification/annual_sum_all_wb/"

data_all =[]

for year in years:
    print(year)
    p = rasterio.open(riskPlumePath+"plume_risk_score_"+year+".tif")
    p_ar = p.read(1)
    data_all.append(p_ar)
    
#create a raster stack
rasterS = np.dstack(data_all)



#sum all the numbers (1s)
stackSum= np.nansum(rasterS, axis=2)


stackSum = stackSum/len(data_all)

#rescale
r_min = np.nanmin(stackSum)
r_max = np.nanmax(stackSum)
 
stackSum_rescale = (stackSum - r_min) / (r_max - r_min)

#turn 0 to nan
stackSum_rescale= np.where(stackSum_rescale == 0, np.nan, stackSum_rescale)

#turn 0 to nan
#stackSum = np.where(stackSum == 0, np.nan, stackSum)

exportTif(templateTif = riskPlumePath+"plume_risk_score_2017.tif" ,
       outputPath = riskPlumePath, 
       outputRasterName = "plume_risk_score_2017_2021_rescaled_mean.tif", 
       arrayExport = stackSum,_rescale 
       na_val = np.nan)

