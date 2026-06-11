# Cybersecurity Threats Assessment

![Dashboard Demo](assets/streamlit-dashboard.gif)


## Overview

Serangan siber menjadi salah satu ancaman utama bagi organisasi modern karena dapat menyebabkan kerugian finansial, gangguan operasional, serta risiko keamanan informasi. Proyek ini bertujuan untuk menganalisis pola serangan siber global, membangun kerangka penilaian risiko (*risk assessment*), serta mengevaluasi kemampuan model machine learning dalam memprediksi kategori risiko serangan berdasarkan karakteristik serangan yang tersedia pada dataset.

Selain analisis dan pemodelan, proyek ini juga dilengkapi dengan dashboard interaktif menggunakan Streamlit untuk memvisualisasikan pola serangan dan insight utama secara eksploratif.

---

## Research Questions

1. Bagaimana distribusi pola serangan siber berdasarkan negara, jenis serangan, industri target, sumber serangan, dan jenis kerentanan yang dieksploitasi?

2. Seberapa andal kategori risiko serangan (Low/Medium/High) dapat diprediksi dari karakteristik serangan menggunakan model klasifikasi machine learning?

---

## Data Quality Logs

* Tidak ditemukan adanya missing value, tipe data yang salah, nilai data yang mencurigakan, maupun duplikasi data.
* Dataset siap digunakan untuk analisis tanpa preprocessing tambahan.
* Fitur `Year` tidak akan dikonversi menjadi date karena pada konteks ini hanya penanda tahun serangan terjadi.

---

## Tujuan EDA & Modelling

Exploratory Data Analysis ini digunakan untuk menggali pola dan insight dari data serta melakukan feature engineering untuk Model Prediksi yaitu Klasifikasi dengan beberapa metode seperti XGBoost, Decision Tree, dan Random Forest Classifier. Klasifikasi ini akan memprediksi Kategori Risiko suatu Serangan (Low/Medium/High) berdasarkan Country, Attack Type, Target Industry, Financial Loss (in Million $), Number of Affected Users, Attack Source, Security Vulnerability Type, Defense Mechanism Used, dan Incident Resolution Time (in Hours).

---

## Feature Engineering

1. Data asli terdiri dari 10 fitur yang mencakup informasi negara, jenis serangan, industri target, dampak finansial, jumlah pengguna terdampak, sumber serangan, jenis kerentanan, mekanisme pertahanan, serta waktu penyelesaian insiden.

2. Seluruh fitur numerik (`Financial Loss`, `Number of Affected Users`, dan `Incident Resolution Time`) dinormalisasi menggunakan MinMaxScaler untuk menyamakan rentang nilai tanpa mengubah distribusi aslinya.

3. Dibentuk `impact_score` menggunakan kombinasi berbobot:

   * Financial Loss (50%)
   * Number of Affected Users (30%)
   * Incident Resolution Time (20%)

4. Dibentuk `attack_likelihood` berdasarkan frekuensi relatif kombinasi unik:

   * Country
   * Attack Type
   * Target Industry
   * Attack Source
   * Security Vulnerability Type

5. Dihitung skor risiko dengan rumus:

   `risk_score = impact_score × attack_likelihood`

6. Risk score kemudian dibagi menjadi tiga kategori menggunakan quantile (1/3 dan 2/3) untuk menghasilkan distribusi label yang seimbang antara kategori Low, Medium, dan High Risk.

---

## Research Findings

### Feature Engineering

Risk score dibangun dari dua komponen: impact_score yang mencerminkan dampak serangan dari sisi finansial, jumlah pengguna terdampak, dan waktu resolusi; serta attack_likelihood yang mencerminkan frekuensi relatif pola serangan berdasarkan kombinasi lima fitur perspektif penyerang. Kombinasi keduanya menghasilkan label risiko yang terdistribusi seimbang (~33% per kelas).

### Model Performance

Tiga model klasifikasi dilatih menggunakan fitur original tanpa risk_score, impact_score, dan likelihood untuk mencegah target leakage. Hasil evaluasi pada test set (20%):

| Model        | Accuracy | F1-macro | Catatan                      |
| ------------ | -------- | -------- | ---------------------------- |
| RandomForest | 55%      | 0.55     | Terbaik, stabil di CV        |
| DecisionTree | 53%      | 0.52     | Rentan overfit tanpa pruning |
| XGBoost      | 51%      | 0.51     | Perlu tuning lebih lanjut    |

Hyperparameter tuning pada RandomForest (36 kombinasi, 5-fold CV) menghasilkan best params `max_depth=None, min_samples_leaf=10, n_estimators=100` dengan CV F1-weighted 0.523 — tidak memberikan peningkatan signifikan dari baseline.

### Keterbatasan Model

Performa model plateau di kisaran 51–55% mengindikasikan bahwa fitur-fitur yang tersedia memiliki sinyal prediktif yang terbatas terhadap Risk Category. Hal ini konsisten dengan temuan EDA bahwa seluruh fitur numerik berdistribusi uniform dan distribusi fitur kategorik hampir seimbang antar kelas. Label Risk Category yang dibentuk dari risk_score mengandung informasi dari fitur-fitur yang sengaja di-drop untuk mencegah leakage, sehingga model memprediksi label dari sinyal yang secara matematis lebih lemah. Ini adalah trade-off yang disadari dalam desain eksperimen ini dan relevan sebagai temuan untuk pengembangan sistem deteksi risiko ke depannya.

---

## Dashboard

Dashboard interaktif tersedia di:

https://global-cybersecurity-threats-assessment.streamlit.app/


### Insight dari Dashboard

#### Financial Loss Overview

Financial Loss per Industri maupun per Negara menunjukkan distribusi yang sangat merata — selisih antara nilai tertinggi dan terendah kurang dari $5B untuk industri (IT ~$24B vs Education ~$20B) dan kurang dari $3B untuk negara (UK ~$16B vs China ~$13.71B). Hal ini mengindikasikan serangan siber tidak mengincar sektor atau wilayah tertentu secara spesifik, melainkan bersifat oportunistik dan tersebar luas.

#### Time Series Analysis

Jumlah serangan maupun rata-rata resolution time keduanya tidak menunjukkan tren yang konsisten — keduanya fluktuatif dari tahun ke tahun tanpa pola naik atau turun yang jelas. Attack count mencapai titik terendah di 2019 dan kembali memuncak di 2022, sementara resolution time bergerak dalam rentang sempit ~35.5–38.5 jam. Ini mengindikasikan bahwa faktor tahun tidak berpengaruh signifikan terhadap kedua metrik ini, konsisten dengan temuan EDA.

#### Attack Distribution

Distribusi Security Vulnerability Type hampir merata di keempat kategori (Zero-day 26.2%, Social Engineering 24.9%, Unpatched Software 24.6%, Weak Passwords 24.3%). Meski selisihnya kecil, Weak Passwords tetap dapat ditekan dengan menerapkan SPO password yang mewajibkan kombinasi karakter kuat dan penggantian berkala, sehingga berpotensi mengurangi ~24.3% vektor serangan yang seharusnya paling mudah dicegah.

Dari sisi Attack Source, Insider threat menyumbang 25.1% — angka yang signifikan mengingat serangan dari dalam jauh lebih sulit dideteksi. Disarankan untuk melakukan pengecekan dan audit akses anggota instansi/organisasi secara berkala guna memitigasi risiko ini sejak dini.

---

## Tools

* Python
* Streamlit
