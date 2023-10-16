import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

##Membuat fungsi untuk memanggil atau membuat data yang diperlukan

def buat_data_bulanan(df):
    data_bulanan=data.groupby(by=["bulan_tahun"]).agg({
    "casual" :  "sum",
    "registered" : "sum",
    "cnt" : "sum"
})
    return data_bulanan

def buat_data_pelanggan(df):
    data_pelanggan=data.groupby(by="yr"). agg({
    "casual" : "sum",
    "registered" : "sum",
})
    return data_pelanggan


##Memuat data yang akan dipakai
data = pd.read_csv("data.csv")

datetime_columns = ["dteday", "bulan_tahun"]

for column in datetime_columns:
    data[column] = pd.to_datetime(data[column])


# Filter data
min_date = data["bulan_tahun"].min()
max_date = data["bulan_tahun"].max()

with st.sidebar:
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = data[(data["bulan_tahun"] >= str(start_date)) & 
                (data["bulan_tahun"] <= str(end_date))]



#Menyiapkan beberapa Datafram
data_bulanan = buat_data_bulanan(data)
data_pelanggan = buat_data_pelanggan(data)

#Perbandingan jumlah peminjaman
st.header("Dashboard Peminjaman Sepeda")
st.subheader("Perbandingan Jumlah Peminjaman")

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
st.pyplot(fig)

#Trend peminjaman bulanan
st.subheader("Tren Peminjaman Sepeda Bulanan")

fig = plt.figure(figsize=(10,5))
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
st.pyplot(fig)

st.caption('Copyright © Syahrul Ghani Abdul Rasyad 2023')