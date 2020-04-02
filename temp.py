from __future__ import print_function
import SimpleITK as sitk
import os,time
import numpy as np

# path = '/home/drbrainer/yupei/StrokeAI/data/TRAINING/case_1/SMIR.Brain.XX.O.CT_CBF.345563/SMIR.Brain.XX.O.CT_CBF.345563.nii' # 3D volume at a certain time
path = '../yupei_data/ISLES2018/ISLES2018_Training/TRAINING/case_3/SMIR.Brain.XX.O.CT_4DPWI.345575/SMIR.Brain.XX.O.CT_4DPWI.345575.nii'
img = sitk.ReadImage(path)
img_arr = sitk.GetArrayFromImage(img)
# print(img.GetOrigin())
# print(img.GetSpacing())
# print(img.GetDirection())
# print(img_arr.shape) #(49, 8, 256, 256)

def writeSlices(series_tag_values, new_img, i):
	img_slice = new_img[:,:,i,:]

	# Tags shared by the series.
	list(map(lambda tag_value: image_slice.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))

	# Slice specific tags.
	image_slice.SetMetaData("0008|0012", time.strftime("%Y%m%d")) # Instance Creation Date
	image_slice.SetMetaData("0008|0013", time.strftime("%H%M%S")) # Instance Creation Time

	# Setting the type to CT preserves the slice location.
	image_slice.SetMetaData("0008|0060", "CT")  # set the type to CT so the thickness is carried over

	# (0020, 0032) image position patient determines the 3D spacing between slices.
	image_slice.SetMetaData("0020|0032", '\\'.join(map(str,new_img.TransformIndexToPhysicalPoint((0,0,i,0))))) # Image Position (Patient)
	image_slice.SetMetaData("0020,0013", str(i)) # Instance Number

	# Write to the output directory and add the extension dcm, to force writing in DICOM format.
	writer.SetFileName(os.path.join(sys.argv[1],str(i)+'.dcm'))
	writer.Execute(image_slice)


new_img = sitk.GetImageFromArray(img_arr)
# print(new_img)
new_img.SetSpacing(img.GetSpacing())
writer = sitk.ImageFileWriter()
writer.KeepOriginalImageUIDOn()


modification_time = time.strftime("%H%M%S")
modification_date = time.strftime("%Y%m%d")

# Copy some of the tags and add the relevant tags indicating the change.
# For the series instance UID (0020|000e), each of the components is a number, cannot start
# with zero, and separated by a '.' We create a unique series ID using the date and time.
# tags of interest:
direction = new_img.GetDirection()
print(direction)
series_tag_values = [("0008|0031",modification_time), # Series Time
                  ("0008|0021",modification_date), # Series Date
                  ("0008|0008","DERIVED\\SECONDARY"), # Image Type
                  ("0020|000e", "1.2.826.0.1.3680043.2.1125."+modification_date+".1"+modification_time), # Series Instance UID
                  ("0020|0037", '\\'.join(map(str, (direction[0], direction[3], direction[6],# Image Orientation (Patient)
                                                    direction[1],direction[4],direction[7])))),
                  ("0008|103e", "Created-SimpleITK")] # Series Description

# Write slices to output directory
list(map(lambda i: writeSlices(series_tag_values, new_img, i), range(new_img.GetDepth())))

# Re-read the series
# Read the original series. First obtain the series file names using the
# image series reader.
data_directory = sys.argv[1]
series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(data_directory)
if not series_IDs:
    print("ERROR: given directory \""+data_directory+"\" does not contain a DICOM series.")
    sys.exit(1)
series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(data_directory, series_IDs[0])

series_reader = sitk.ImageSeriesReader()
series_reader.SetFileNames(series_file_names)


# Configure the reader to load all of the DICOM tags (public+private):
# By default tags are not loaded (saves time).
# By default if tags are loaded, the private tags are not loaded.
# We explicitly configure the reader to load tags, including the
# private ones.
series_reader.LoadPrivateTagsOn()
image3D = series_reader.Execute()
print(image3D.GetSpacing(),'vs',new_img.GetSpacing())
sys.exit( 0 )




# ====================================================================================================================



'''
Python combine multiple .csv files into one csv.file

'''

import os
import glob


csv_list = glob.glob('*.csv')
print('In total %s CSV files.'%len(csv_list))

for i in csv_list:
    fr = open(i, 'rb').read()
    with open('update.csv', 'ab') as f:
        f.write(fr)

print('Finished!')
