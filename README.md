# Cybersecurity Threats Assessment

## Research Questions
1. Bagaimana distribusi pola serangan siber berdasarkan negara, jenis serangan, dan industri yang menjadi target?
2. Faktor-faktor apa saja yang membentuk skor risiko (risk score) suatu serangan siber?
3. Apakah kategori risiko serangan (Low/Medium/High) dapat diprediksi secara andal dari fitur-fitur yang tersedia menggunakan model klasifikasi machine learning?

## Data Quality Logs
* Tidak ditemukan adanya missing value, tipe data yang salah, nilai data yang mencurigakan, maupun duplikasi data.
* Dataset siap digunakan untuk analisis tanpa preprocessing tambahan.
* Fitur `Year` tidak akan dikonversi menjadi date karena pada konteks ini hanya penanda tahun serangan terjadi.

## Tujuan EDA & Modelling
Exploratory Data Analysis ini digunakan untuk menggali pola dan insight dari data serta melakukan feature engineering untuk Model Prediksi yaitu Klasifikasi dengan beberapa metode seperti XGBoost, Decision Tree, dan Random Forest Classifier. Klasifikasi ini akan memprediksi Kategori Risiko suatu Serangan (Low/Medium/High) berdasarkan Country, Attack Type, Target Industry, Financial Loss (in Million $), Number of Affected Users, Attack Source, Security Vulnerability Type, Defense Mechanism Used, dan Incident Resolution Time (in Hours).

## Insight dari Data
1. Data asli memiliki 10 kolom yang mencakup: Country, Year, Attack Type, Target Industry, Financial Loss (in Million $), Number of Affected Users, Attack Source, Security Vulnerability Type, Defense Mechanism Used, Incident Resolution Time (in Hours) dan berdasarkan pengecekan awal data sudah bersih untuk dilakukan EDA.
2. Eksplorasi distribusi kolom numerik yaitu Financial Loss, Number of Affected Users, dan Incident Resolution Time menunjukkan seluruh kolom numerik berdistribusi uniform.
3. Dilakukan feature engineering yaitu MinMaxScaler pada seluruh kolom numerik (untuk menyamakan rentang nilai antar kolom numerik ke skala 0–1 tanpa mengubah bentuk distribusi aslinya), lalu membuat kolom impact_score = $0.5\times$ Financial Loss $+ 0.3\times$ Number of Affected Users $+ 0.2\times$ Incident Resolution Time.
4. Eksplorasi distribusi fitur-fitur kategorik yang mencakup: Country, Attack Type, Target Industry, Attack Source, Security Vulnerability Type, Defense Mechanism Used menunjukkan distribusi tiap kolom cukup seimbang dengan selisih jumlah kelas terbesar dan terkecil < 100.
5. Pengecekan time-series tahunan terkait Sum of Attacks dan Incident Resolution Time menunjukkan tidak ada indikator khusus bahwa fitur Year berpengaruh terhadap pola serangan.
6. Dilakukan agregasi secara count untuk membentuk `attack_likelihood` yang merepresentasikan peluang munculnya suatu pola serangan berdasarkan kombinasi unik Country × Attack Type × Target Industry × Attack Source × Security Vulnerability Type. Pemilihan kelima fitur ini didasarkan pada perspektif penyerang (*attacker's perspective*) — Country mencerminkan asal dan target geografis, Attack Type mencerminkan metode yang digunakan, Target Industry mencerminkan sektor yang disasar, Attack Source mencerminkan vektor serangan, dan Security Vulnerability Type mencerminkan celah yang dieksploitasi. Likelihood dihitung sebagai frekuensi relatif (count/total rows) dari setiap kombinasi unik kelima fitur tersebut.
7. `attack_likelihood` di-merge kembali ke dataset utama.
8. Dihitung skor risiko dimana risk_score = impact_score $\times$ likelihood, kemudian divisualisasikan distribusinya beserta batas kuantil 1/3 dan 2/3. Pembagian berdasarkan quantile dipilih untuk memastikan distribusi label Low/Medium/High yang seimbang (~33% tiap kelas), yang penting untuk training model klasifikasi.

## Research Findings

### Feature Engineering
Risk score dibangun dari dua komponen: impact_score yang mencerminkan dampak serangan dari sisi finansial, jumlah pengguna terdampak, dan waktu resolusi; serta attack_likelihood yang mencerminkan frekuensi relatif pola serangan berdasarkan kombinasi lima fitur perspektif penyerang. Kombinasi keduanya menghasilkan label risiko yang terdistribusi seimbang (~33% per kelas).

### Model Performance
Tiga model klasifikasi dilatih menggunakan fitur original tanpa risk_score, impact_score, dan likelihood untuk mencegah target leakage. Hasil evaluasi pada test set (20%):

| Model | Accuracy | F1-macro | Catatan |
|---|---|---|---|
| RandomForest | 55% | 0.55 | Terbaik, stabil di CV |
| DecisionTree | 53% | 0.52 | Rentan overfit tanpa pruning |
| XGBoost | 51% | 0.51 | Perlu tuning lebih lanjut |

Hyperparameter tuning pada RandomForest (36 kombinasi, 5-fold CV) menghasilkan best params `max_depth=None, min_samples_leaf=10, n_estimators=100` dengan CV F1-weighted 0.523 — tidak memberikan peningkatan signifikan dari baseline.

### Keterbatasan Model
Performa model plateau di kisaran 51–55% mengindikasikan bahwa fitur-fitur yang tersedia memiliki sinyal prediktif yang terbatas terhadap Risk Category. Hal ini konsisten dengan temuan EDA bahwa seluruh fitur numerik berdistribusi uniform dan distribusi fitur kategorik hampir seimbang antar kelas. Label Risk Category yang dibentuk dari risk_score mengandung informasi dari fitur-fitur yang sengaja di-drop untuk mencegah leakage, sehingga model memprediksi label dari sinyal yang secara matematis lebih lemah. Ini adalah trade-off yang disadari dalam desain eksperimen ini dan relevan sebagai temuan untuk pengembangan sistem deteksi risiko ke depannya.

## Dashboard

## Tools
* Python
* Excel
