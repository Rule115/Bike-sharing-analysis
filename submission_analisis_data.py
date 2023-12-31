# -*- coding: utf-8 -*-
"""Submission Analisis Data

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16mpTvVKo0Q8VAHKHPfuW55M5pB7BejbE

# Proyek Analisis Data: Nama dataset
- Nama: Syahrul Ghani Abdul Rasyad
- Email: abdul15rasyad@gmail.com
- Id Dicoding: Syahrul Ghani Abdul Rasyad

## Menentukan Pertanyaan Bisnis

- Bagaimana trend bulanan peminjaman sepeda?
- Bagaimana perbandingan jumlah peminjaman pelanggan casual dan registered?

## Menyaipkan semua library yang dibuthkan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

"""## Data Wrangling

### Gathering Data
"""

! pip install -q kaggle

! mkdir ~/.kaggle

! cp kaggle.json ~/.kaggle/

! chmod 600 ~/.kaggle/kaggle.json

! kaggle datasets download lakshmi25npathi/bike-sharing-dataset

import zipfile
with zipfile.ZipFile("/content/bike-sharing-dataset.zip", 'r') as zip_ref:
    zip_ref.extractall("/content")

data=pd.read_csv("day.csv")
data.head(5)

"""### Assessing Data

CEK DATA TIAP FEATURE
"""

data.info()

"""Dari hasil cek tipe data, didapatkan :


1.   Ubah format dteday kedalam datetime
2.   Tidak diindikasikan terdapat missing value

CEK DUPLIKASI DATA
"""

#cek duplikasi data
duplikasi = data.duplicated().sum()
print("jumlah data duplikasi yang ada : ", duplikasi)

"""CEK NILAI DATA YANG TIDAK RELEVANT"""

data.describe()

"""ubah nilai data dari yr, mnth, dan season menjadi seharusnya (tidak diwakili angka) agar lebih jelas saat divisulisasikan

### Cleaning Data

#### MENGUBAH TIPE DATA
"""

#Mengubah tipe data dteday menjadi datetime
datetime_columns = ["dteday"]

for column in datetime_columns:
  data[column] = pd.to_datetime(data[column])

#Mengekstrak bulan-tahun dari dteday
bulan_tahun=data["dteday"].dt.strftime("%m-%Y")
data["bulan_tahun"]=bulan_tahun

#Mengubah tipe data bulan_tahun menjadi datetime
datetime_columns = ["bulan_tahun"]

for column in datetime_columns:
  data[column] = pd.to_datetime(data[column])

data.info()

"""## Exploratory Data Analysis (EDA)

### Explore Data Peminjaman Perbulan
"""

#Group data berdasarkan bulan dan tahun
data_bulanan=data.groupby(by=["bulan_tahun"]).agg({
    "casual" :  "sum",
    "registered" : "sum",
    "cnt" : "sum"
})

print(data_bulanan)

data_pelanggan=data.groupby(by="yr"). agg({
    "casual" : "sum",
    "registered" : "sum",
})

"""## Visualization & Explanatory Analysis

### Pertanyaan 1:

*   Bagaimana trend bulanan peminjaman sepeda?
"""

plt.figure(figsize=(10,5))
sns.lineplot(
    data=data_bulanan,
    x="bulan_tahun",
    y="cnt",
    label="Jumlah Total"
)
sns.lineplot(
    data=data_bulanan,
    x="bulan_tahun",
    y="casual",
    label="Casual"
)
sns.lineplot(
    data=data_bulanan,
    x="bulan_tahun",
    y="registered",
    label="Registered"
)
plt.title("Trend Peminjaman Bulanan")
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.legend()
plt.show

"""### Pertanyaan 2:

*   Bagaimana perbandingan jumlah peminjaman pelanggan casual dan registered?




"""

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

ax[0].pie(
    x= data_pelanggan.iloc[0],
    labels=["casual","registered"],
    autopct='%1.1f%%',
    colors=('#8B4513', '#93C572'),

)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Tahun 2011", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

ax[1].pie(
    x= data_pelanggan.iloc[1],
    labels=["casual","registered"],
    autopct='%1.1f%%',
    colors=('#8B4513', '#93C572'),
    #ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].yaxis.set_label_position("right")
ax[1].set_title("Tahun 2012", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("Perbandingan Jumlah Peminjaman Pelanggan Casual dan Registered", fontsize=20)
plt.show()

"""## Conclusion

- Conclution "Bagaimana trend bulanan peminjaman sepeda"


1.   Untuk tahun 2011, Peminjaman sepeda akan meningkat dan mencapai puncaknya ketika dipertengahan tahun antara bulan mei dan juni, lalu akan kembali menurun sampai dengan akhir tahun

2.   Untuk tahun 2012, sama seperti tahun 2011 hanya saja puncak peminjaman berada pada antara bulan agustus dan september

2.   Total peminjaman pada tahun 2012 cenderung lebih banyak dari tahun 2011

3.   Total pemnijaman untuk pelanggan resgistered lebih banyak daripada pelanggan casual


- conclution "Bagaimana perbandingan jumlah peminjaman pelanggan casual dan registered?"


1.   Baik untuk tahun 2011 maupun 2012, Jumlah peminjaman pelanggan rregistered lebih banyak dari pada casual dengan proporsi peminjaman yang sangat jauh.
"""

data.to_csv("data.csv", index=False)