import SimpleITK as sitk

file_path = '../data/CTP/LIU/DICOM'
txt_path = '../data/CTP/LIU/series.txt'
nii_path = '../data/CTP/LIU/perfusiondd_'+file_path.split('/')[-2]+'.nii'

series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(file_path)
print('\n'.join(series_IDs))
nb_series = len(series_IDs)
print(nb_series)

with open(txt_path,'w+') as f:
    f.writelines('\n'.join(series_IDs))

series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(file_path, series_IDs[1])
print('\n'.join(series_file_names))
print(len(series_file_names))

series_file_names = list(series_file_names)
series_file_names.sort(key=lambda x:int(sitk.ReadImage(x).GetMetaData(key='0020|0013')))

origins = []
c = []
for x in series_file_names:
    print(x,sitk.ReadImage(x).GetMetaData(key='0020|0013'))
    d = sitk.ReadImage(x).GetOrigin()[2]  # x, y ,z
    print(d)
    if not d in origins:
        origins.append(d)
        c.append(1)
    else:
        c[origins.index(d)] += 1
print(origins)
print(c)

series_reader = sitk.ImageSeriesReader()
series_reader.SetFileNames(series_file_names)
image3D = series_reader.Execute()
array = sitk.GetArrayFromImage(image3D)
print(array.shape)
n = len(series_file_names)
w = len(origins)
x = array.shape[1]
y = array.shape[2]

img = sitk.GetImageFromArray(array)
sitk.WriteImage(img, nii_path)
