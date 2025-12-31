# 🚗 Araba Uzmanı ChatBot

Araba ve araç sorunları konusunda uzman bir yapay zeka asistanı. Streamlit ile geliştirilmiş, LangChain ile Google Gemini ve OpenAI ChatGPT API entegrasyonu sağlanmış, Intent Classification ile gelişmiş bir ChatBot uygulaması.

## ✨ Özellikler

### 🎯 Ana Özellikler
- **Araba Sorunları Uzmanı**: Sadece araba ve araç sorunları hakkında uzmanlaşmış AI asistanı
- **Çoklu Model Desteği**: Gemini ve ChatGPT arasında seçim yapabilme
- **Intent Classification**: TF-IDF tabanlı otomatik kategori tespiti (11 kategori)
- **Kategori Bazlı Sorular**: 6 farklı kategori ile hızlı erişim
  - 🔧 Motor Sorunları
  - 🛞 Fren Sistemleri
  - ⚡ Elektrik & Akü
  - 🌡️ Klima & Isıtma
  - ⚙️ Şanzıman
  - 🔍 Bakım İpuçları
- **Sohbet Geçmişi**: Tüm sohbetlerinizi kaydedin ve istediğiniz zaman geri dönün
- **Doküman Desteği**: PDF, DOCX, XLSX dosyalarından bilgi çekme
- **Modern UI**: Koyu tema ve gradient renklerle tasarlanmış kullanıcı dostu arayüz

### 🧠 Intent Classification Sistemi
- **987 eğitim örneği** ile eğitilmiş TF-IDF tabanlı sınıflandırıcı
- **11 kategori**: motor, fren, elektrik, klima, şanzıman, lastik, süspansiyon, egzoz, bakım, selamlama, kapsam_dışı
- **Otomatik kategori tespiti**: Her kullanıcı sorusu için intent ve güven skoru hesaplanır
- **Değerlendirme metrikleri**: Precision, Recall, F1 Score

### Örnen Kullanım ve Arayüz
![Ekran görüntüsü_31-12-2025_123358_localhost](https://github.com/user-attachments/assets/0a80647d-327b-455c-bc36-12b793e4d9d6)

![Ekran görüntüsü_31-12-2025_123420_localhost](https://github.com/user-attachments/assets/5c649bf1-0cee-4ac9-8938-e6fdf429d98f)

![Ekran görüntüsü_31-12-2025_123737_localhost](https://github.com/user-attachments/assets/516d649a-045d-4162-a819-334463b4435d)

![Ekran görüntüsü_31-12-2025_124053_localhost](https://github.com/user-attachments/assets/a4f6b9d6-2d7f-4ef3-be35-ff0cfe7e155e)



https://github.com/user-attachments/assets/581137e2-8d09-45b3-91d5-1f0aec738cc3




 
### 📊 Model Performansı

| Metrik | Değer |
|--------|-------|
| Accuracy | 61.82% |
| Macro Precision | 78.16% |
| Macro Recall | 61.82% |
| Macro F1 Score | 65.08% |

### 🔒 Güvenlik
- API anahtarları `.env` dosyasında güvenli şekilde saklanır
- Hassas bilgiler git'e commit edilmez

## � Proje Akış Diyagramı

![ChatBot Akış Diyagramı](flow_diagram.png)

## �📋 Gereksinimler

- Python 3.8+
- Google Gemini API anahtarı
- OpenAI API anahtarı (opsiyonel, ChatGPT kullanmak için)

## 🚀 Kurulum

### 1. Projeyi Klonlayın veya İndirin

```bash
cd "proje-klasörü-yolu"
```

### 2. Bağımlılıkları Yükleyin

```bash
pip3 install -r requirements.txt
```

### 3. API Anahtarlarını Ayarlayın

`.env` dosyası oluşturun:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

**API Anahtarları Nasıl Alınır?**

**Gemini:**
1. [Google AI Studio](https://aistudio.google.com/app/apikey) adresine gidin
2. "Create API Key" butonuna tıklayın

**OpenAI:**
1. [OpenAI Platform](https://platform.openai.com/api-keys) adresine gidin
2. "Create new secret key" butonuna tıklayın

### 4. Uygulamayı Başlatın

```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` adresinde açılacaktır.

## 🏗️ Proje Yapısı

```
ChatBot Odev/
├── app.py                    # Ana Streamlit uygulaması
├── gemini_client.py          # LangChain + Gemini/OpenAI API entegrasyonu
├── intent_classifier.py      # TF-IDF tabanlı Intent Classification modülü
├── evaluate_intent.py        # Değerlendirme metrikleri (Precision, Recall, F1)
├── document_processor.py     # Doküman işleme modülü
├── intents.txt               # Eğitim verisi (987 örnek, 11 kategori)
├── test_intents.txt          # Test verisi (220 örnek, bağımsız)
├── evaluation_report.txt     # Değerlendirme raporu
├── requirements.txt          # Python bağımlılıkları
├── documents/                # Doküman klasörü (PDF, DOCX, XLSX)
├── .env                      # API anahtarları (oluşturulmalı)
├── .env.example              # API anahtarları örneği
├── .gitignore                # Git ignore dosyası
└── README.md                 # Bu dosya
```

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|-----------|----------|
| **Streamlit** | Web arayüzü framework'ü |
| **LangChain** | LLM entegrasyonu ve sohbet yönetimi |
| **Google Gemini API** | AI modeli (gemini-2.5-flash) |
| **OpenAI API** | AI modeli (gpt-4o) |
| **TF-IDF** | Intent Classification için vektörizasyon |
| **python-dotenv** | Ortam değişkenleri yönetimi |

### Intent Classification Mimarisi

```
Kullanıcı Mesajı
      ↓
Tokenization (kelime ayırma)
      ↓
TF-IDF Vektörizasyon
      ↓
Cosine Similarity (her kategori ile)
      ↓
En yüksek benzerlik → Tahmin edilen Intent
```

### Değerlendirme Çalıştırma

```bash
python3 evaluate_intent.py
```

Bu komut:
- Test verisini yükler (`test_intents.txt`)
- Her örnek için intent tahmini yapar
- Precision, Recall, F1 Score hesaplar
- Confusion matrix oluşturur
- Raporu `evaluation_report.txt` dosyasına kaydeder

## 📸 Kullanım

### Model Seçimi
Sidebar'da "Model Seçimi" bölümünden:
- **Gemini**: Google'ın Gemini 2.5 Flash modeli
- **ChatGPT**: OpenAI'ın GPT-4o modeli

### Intent Görüntüleme
Her bot yanıtının altında tespit edilen kategori ve güven skoru görüntülenir:
```
📌 🔧 Motor Sorunları (75%)
```

### Örnek Sorular

- "Arabamın motoru çalışmıyor, ne yapmalıyım?"
- "Fren pedalı sertleşti, nedeni ne olabilir?"
- "Klima soğutmuyor ne yapmalıyım?"
- "Vites geçerken ses geliyor"
- "Akü ne sıklıkla değiştirilmeli?"

## ⚠️ Önemli Notlar

1. **API Anahtarı Güvenliği**: `.env` dosyasını asla git'e commit etmeyin
2. **API Limitleri**: API kullanım limitlerine dikkat edin
3. **Sadece Araba Sorunları**: ChatBot sadece araba ve araç sorunları hakkında uzmandır
4. **Profesyonel Tavsiye**: Ciddi araç sorunlarında mutlaka profesyonel servise danışın

## 🐛 Sorun Giderme

### API Anahtarı Bulunamadı

```
ValueError: GEMINI_API_KEY bulunamadı!
```

**Çözüm**: `.env` dosyasını kontrol edin.

### OpenAI Kota Hatası

```
Error code: 429 - insufficient_quota
```

**Çözüm**: OpenAI hesabınıza kredi ekleyin veya Gemini modelini kullanın.

### Modül Bulunamadı

```bash
pip3 install -r requirements.txt
```

## 🔄 Güncellemeler

- **v2.0**: Gelişmiş Özellikler
  - ✅ Intent Classification sistemi (TF-IDF)
  - ✅ 987 eğitim örneği, 11 kategori
  - ✅ Değerlendirme metrikleri (Precision, Recall, F1)
  - ✅ Ayrı test seti (220 örnek)
  - ✅ ChatGPT (OpenAI) desteği
  - ✅ Model seçimi (Gemini/ChatGPT)
  - ✅ Intent badge görüntüleme

- **v1.0**: İlk sürüm
  - ✅ Temel ChatBot özellikleri
  - ✅ Kategori bazlı sorular (6 kategori)
  - ✅ Sohbet geçmişi yönetimi
  - ✅ Modern UI tasarımı
  - ✅ LangChain entegrasyonu
  - ✅ Doküman işleme

---

**🚗 Araba Uzmanı ChatBot** - Arabanızla ilgili her türlü teknik soruda yanınızdayım!
