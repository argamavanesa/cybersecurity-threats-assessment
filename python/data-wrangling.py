import numpy as np
import pandas as pd

#Load dataset
df = pd.read_csv('../data/raw-data.csv')

#Cek beberapa baris pertama dari dataset
print("Beberapa baris pertama dari dataset:")
print(df.head())

#Cek info dataset
print("Informasi dataset:")
df.info()

#Cek rangkuman statistik dari dataset
print ("Rangkuman statistik dataset:")
print(df.describe(include='all'))

# Print number of duplicate rows
duplicate_count = df.duplicated().sum()
print("Number of duplicate rows:", duplicate_count)

/* 
Logs:
1. Tidak ditemukan adanya missing value, tipe data yang salah, nilai data yang mencurigakan, maupun duplikasi data.
2. Dataset siap digunakan untuk analisis tanpa preprocessing tambahan
3. Fitur `Year`tidak akan dikonversi menjadi date karena pada konteks ini hanya penanda tahun serangan terjadi.
*/
