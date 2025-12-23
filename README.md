# 🚗 Araba Uzmanı ChatBot

Araba ve araç sorunları konusunda uzman bir yapay zeka asistanı. Streamlit ile geliştirilmiş, LangChain ve Google Gemini API kullanılarak oluşturulmuş modern bir ChatBot uygulaması.

## ✨ Özellikler

### 🎯 Ana Özellikler
- **Araba Sorunları Uzmanı**: Sadece araba ve araç sorunları hakkında uzmanlaşmış AI asistanı
- **Kategori Bazlı Sorular**: 6 farklı kategori ile hızlı erişim
  - 🔧 Motor Sorunları
  - 🛞 Fren Sistemleri
  - ⚡ Elektrik & Akü
  - 🌡️ Klima & Isıtma
  - ⚙️ Şanzıman
  - 🔍 Bakım İpuçları
- **Sohbet Geçmişi**: Tüm sohbetlerinizi kaydedin ve istediğiniz zaman geri dönün
- **Modern UI**: Koyu tema ve gradient renklerle tasarlanmış kullanıcı dostu arayüz
- **Akıllı Filtreleme**: Araba dışı konularda (sağlık, yemek, programlama vb.) yanıt vermez

### 🔒 Güvenlik
- API anahtarı `.env` dosyasında güvenli şekilde saklanır
- Hassas bilgiler git'e commit edilmez

## 📋 Gereksinimler

- Python 3.8+
- Google Gemini API anahtarı

## 🚀 Kurulum

### 1. Projeyi Klonlayın veya İndirin

Proje klasörüne gidin:
```bash
cd "proje-klasörü-yolu"
```

### 2. Bağımlılıkları Yükleyin

```bash
pip3 install -r requirements.txt
```

### 3. API Anahtarını Ayarlayın

1. `.env` dosyası oluşturun:
```bash
touch .env
```

2. `.env` dosyasına API anahtarınızı ekleyin:
```
GEMINI_API_KEY=your_api_key_here
```

**API Anahtarı Nasıl Alınır?**
1. [Google AI Studio](https://aistudio.google.com/app/apikey) adresine gidin
2. "Create API Key" butonuna tıklayın
3. Anahtarı kopyalayıp `.env` dosyasına yapıştırın

### 4. Uygulamayı Başlatın

```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` adresinde açılacaktır.

## 📖 Kullanım

### İlk Kullanım

1. Uygulamayı başlattıktan sonra ana sayfada hoş geldin mesajı ve kategori butonları görünecektir
2. İstediğiniz kategoriye tıklayarak o konuyla ilgili sık sorulan soruları görebilirsiniz
3. Veya doğrudan chat input alanına sorunuzu yazabilirsiniz

### Sohbet Geçmişi

- **Sol sidebar'ı açın**: Sayfanın sol üst köşesindeki `>` ikonuna tıklayın
- **Yeni sohbet başlatın**: "➕ Yeni Sohbet" butonuna tıklayın
- **Eski sohbetleri görüntüleyin**: Listeden istediğiniz sohbeti seçin
- **Sohbet silme**: Her sohbetin yanındaki 🗑️ butonuna tıklayın

### Örnek Sorular

- "Arabamın motoru çalışmıyor, ne yapmalıyım?"
- "Fren pedalı sertleşti, nedeni ne olabilir?"
- "Araç ısınıyor ama kalorifer çalışmıyor"
- "Vites geçerken ses geliyor"
- "Akü ne sıklıkla değiştirilmeli?"

## 🏗️ Proje Yapısı

```
ChatBot Odev/
├── app.py                 # Ana Streamlit uygulaması
├── gemini_client.py      # LangChain + Gemini API entegrasyonu
├── requirements.txt       # Python bağımlılıkları
├── .env                  # API anahtarı (oluşturulmalı, git'e commit edilmez)
├── .gitignore            # Git ignore dosyası
└── README.md             # Bu dosya
```

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler

- **Streamlit**: Web arayüzü framework'ü
- **LangChain**: LLM entegrasyonu ve sohbet yönetimi
- **Google Gemini API**: AI modeli (gemini-2.5-flash)
- **python-dotenv**: Ortam değişkenleri yönetimi

### Mimari

- **Frontend**: Streamlit ile responsive web arayüzü
- **Backend**: LangChain ile AI model entegrasyonu
- **State Management**: Streamlit session state ile sohbet geçmişi yönetimi
- **API**: Google Gemini API ile doğal dil işleme

### Özellikler

- **Kategori Filtreleme**: Sadece araba sorunları hakkında yanıt verir
- **Selamlaşma Desteği**: "Merhaba", "Nasılsın" gibi selamlamalara yanıt verir
- **Yasaklı Konular**: Sağlık, yemek, programlama, siyaset gibi konularda yanıt vermez
- **Sohbet Geçmişi**: Tüm sohbetler otomatik kaydedilir ve geri yüklenebilir
- **Gerçek Zamanlı Yanıt**: Gemini API ile anlık ve akıllı yanıtlar

## ⚠️ Önemli Notlar

1. **API Anahtarı Güvenliği**: `.env` dosyasını asla git'e commit etmeyin
2. **API Limitleri**: Google Gemini API'nin kullanım limitlerine dikkat edin
3. **Sadece Araba Sorunları**: ChatBot sadece araba ve araç sorunları hakkında uzmandır
4. **Profesyonel Tavsiye**: Ciddi araç sorunlarında mutlaka profesyonel servise danışın

## 🐛 Sorun Giderme

### API Anahtarı Bulunamadı Hatası

```
ValueError: GEMINI_API_KEY bulunamadı!
```

**Çözüm**: `.env` dosyasının proje kök dizininde olduğundan ve doğru formatta olduğundan emin olun:
```
GEMINI_API_KEY=your_api_key_here
```

### Modül Bulunamadı Hatası

```
ModuleNotFoundError: No module named 'langchain'
```

**Çözüm**: Tüm bağımlılıkları yükleyin:
```bash
pip3 install -r requirements.txt
```

### Port Zaten Kullanımda

```
Port 8501 is already in use
```

**Çözüm**: Farklı bir port kullanın:
```bash
streamlit run app.py --server.port 8502
```

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 👨‍💻 Geliştirici

Araba sorunları konusunda uzman AI asistanı - Streamlit + LangChain + Gemini API

## 🔄 Güncellemeler

- **v1.0**: İlk sürüm
  - ✅ Temel ChatBot özellikleri
  - ✅ Kategori bazlı sorular (6 kategori)
  - ✅ Sohbet geçmişi yönetimi (sidebar)
  - ✅ Modern UI tasarımı (koyu tema)
  - ✅ LangChain entegrasyonu
  - ✅ API anahtarı güvenliği (.env)
  - ✅ Akıllı konu filtreleme

---

**🚗 Araba Uzmanı ChatBot** - Arabanızla ilgili her türlü teknik soruda yanınızdayım!
