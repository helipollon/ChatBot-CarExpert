"""
Intent Classification Module
Kullanıcı mesajlarını kategorilere ayıran sınıflandırıcı.
TF-IDF + Naive Bayes kullanarak intent tespiti yapar.
"""

import os
import re
from typing import Tuple, List, Dict
from collections import defaultdict
import math


class IntentClassifier:
    """TF-IDF tabanlı Intent Sınıflandırıcı"""
    
    # Intent açıklamaları
    INTENT_DESCRIPTIONS = {
        "motor": "🔧 Motor Sorunları",
        "fren": "🛞 Fren Sistemi",
        "elektrik": "⚡ Elektrik & Akü",
        "klima": "🌡️ Klima & Isıtma",
        "sanziman": "⚙️ Şanzıman & Vites",
        "lastik": "🚗 Lastik & Jant",
        "suspansiyon": "🔩 Süspansiyon & Direksiyon",
        "egzoz": "💨 Egzoz & Emisyon",
        "bakim": "🔍 Bakım & Genel",
        "selamlama": "👋 Selamlama",
        "kapsam_disi": "❌ Kapsam Dışı"
    }
    
    def __init__(self, data_file: str = "intents.txt"):
        """
        Intent Classifier başlatıcı
        
        Args:
            data_file: Eğitim verisi dosyası yolu
        """
        self.data_file = data_file
        self.training_data: List[Tuple[str, str]] = []
        self.intent_docs: Dict[str, List[str]] = defaultdict(list)
        
        # TF-IDF için
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.intent_vectors: Dict[str, Dict[str, float]] = {}
        
        # Eğitim verisini yükle
        self._load_training_data()
        self._build_vocabulary()
        self._compute_idf()
        self._compute_intent_vectors()
    
    def _load_training_data(self):
        """Eğitim verisini dosyadan yükler"""
        if not os.path.exists(self.data_file):
            print(f"Uyarı: {self.data_file} bulunamadı!")
            return
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Boş satır veya yorum satırı atla
                if not line or line.startswith('#'):
                    continue
                
                # Format: intent|örnek_cümle
                if '|' in line:
                    parts = line.split('|', 1)
                    if len(parts) == 2:
                        intent, text = parts
                        intent = intent.strip().lower()
                        text = text.strip().lower()
                        self.training_data.append((intent, text))
                        self.intent_docs[intent].append(text)
        
        print(f"✅ {len(self.training_data)} eğitim örneği yüklendi.")
        print(f"📊 Kategoriler: {list(self.intent_docs.keys())}")
    
    def _tokenize(self, text: str) -> List[str]:
        """Metni kelimelere ayırır"""
        # Küçük harfe çevir
        text = text.lower()
        # Türkçe karakterleri koru, alfanumerik ve boşluk dışındakileri kaldır
        text = re.sub(r'[^\w\sğüşıöçĞÜŞİÖÇ]', ' ', text)
        # Boşluklara göre ayır
        tokens = text.split()
        # Kısa kelimeleri filtrele (1 karakterden kısa)
        tokens = [t for t in tokens if len(t) > 1]
        return tokens
    
    def _build_vocabulary(self):
        """Kelime dağarcığı oluşturur"""
        word_idx = 0
        for intent, text in self.training_data:
            tokens = self._tokenize(text)
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary[token] = word_idx
                    word_idx += 1
        
        print(f"📚 Kelime dağarcığı: {len(self.vocabulary)} kelime")
    
    def _compute_idf(self):
        """IDF (Inverse Document Frequency) hesaplar"""
        N = len(self.training_data)  # Toplam doküman sayısı
        
        # Her kelimenin kaç dokümanda geçtiğini say
        doc_freq: Dict[str, int] = defaultdict(int)
        for intent, text in self.training_data:
            tokens = set(self._tokenize(text))
            for token in tokens:
                doc_freq[token] += 1
        
        # IDF hesapla: log(N / df)
        for word, df in doc_freq.items():
            self.idf[word] = math.log(N / (df + 1)) + 1  # Smoothing
    
    def _compute_tf(self, tokens: List[str]) -> Dict[str, float]:
        """TF (Term Frequency) hesaplar"""
        tf: Dict[str, float] = defaultdict(float)
        total = len(tokens)
        if total == 0:
            return tf
        
        for token in tokens:
            tf[token] += 1
        
        # Normalize
        for token in tf:
            tf[token] /= total
        
        return tf
    
    def _compute_tfidf(self, text: str) -> Dict[str, float]:
        """TF-IDF vektörü hesaplar"""
        tokens = self._tokenize(text)
        tf = self._compute_tf(tokens)
        
        tfidf: Dict[str, float] = {}
        for word, tf_val in tf.items():
            idf_val = self.idf.get(word, 1.0)
            tfidf[word] = tf_val * idf_val
        
        return tfidf
    
    def _compute_intent_vectors(self):
        """Her intent için ortalama TF-IDF vektörü hesaplar"""
        for intent, docs in self.intent_docs.items():
            # Intent için tüm dokümanların TF-IDF'lerini topla
            combined: Dict[str, float] = defaultdict(float)
            for doc in docs:
                tfidf = self._compute_tfidf(doc)
                for word, val in tfidf.items():
                    combined[word] += val
            
            # Ortalamasını al
            num_docs = len(docs)
            for word in combined:
                combined[word] /= num_docs
            
            self.intent_vectors[intent] = dict(combined)
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """İki vektör arasındaki kosinüs benzerliğini hesaplar"""
        # Ortak kelimeler
        common_words = set(vec1.keys()) & set(vec2.keys())
        
        if not common_words:
            return 0.0
        
        # Dot product
        dot_product = sum(vec1[w] * vec2[w] for w in common_words)
        
        # Magnitude
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def classify(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Metni sınıflandırır
        
        Args:
            text: Sınıflandırılacak metin
            
        Returns:
            (tahmin_edilen_intent, güven_skoru, tüm_skorlar)
        """
        # Girdi vektörünü hesapla
        input_vector = self._compute_tfidf(text)
        
        if not input_vector:
            # Boş veya çok kısa metin
            return "selamlama", 0.5, {"selamlama": 0.5}
        
        # Her intent ile benzerlik hesapla
        scores: Dict[str, float] = {}
        for intent, intent_vec in self.intent_vectors.items():
            similarity = self._cosine_similarity(input_vector, intent_vec)
            scores[intent] = similarity
        
        # En yüksek skoru bul
        if not scores:
            return "kapsam_disi", 0.0, {}
        
        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]
        
        # Düşük güvende varsayılan davranış
        if best_score < 0.1:
            # Çok düşük benzerlik - muhtemelen genel soru veya selamlama
            return "selamlama", best_score, scores
        
        return best_intent, best_score, scores
    
    def get_intent_description(self, intent: str) -> str:
        """Intent için açıklama döndürür"""
        return self.INTENT_DESCRIPTIONS.get(intent, "❓ Bilinmeyen")
    
    def get_top_intents(self, text: str, top_n: int = 3) -> List[Tuple[str, float]]:
        """En olası N intent'i döndürür"""
        _, _, scores = self.classify(text)
        sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_intents[:top_n]
    
    def is_car_related(self, text: str) -> bool:
        """Metnin araba ile ilgili olup olmadığını kontrol eder"""
        intent, score, _ = self.classify(text)
        
        # Araba ile ilgili intent'ler
        car_intents = {"motor", "fren", "elektrik", "klima", "sanziman", 
                       "lastik", "suspansiyon", "egzoz", "bakim"}
        
        return intent in car_intents and score > 0.15
    
    def get_category_keywords(self, intent: str) -> List[str]:
        """Bir kategori için anahtar kelimeleri döndürür"""
        if intent not in self.intent_vectors:
            return []
        
        vec = self.intent_vectors[intent]
        # En yüksek TF-IDF değerine sahip kelimeleri döndür
        sorted_words = sorted(vec.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:20]]


# Test için
if __name__ == "__main__":
    classifier = IntentClassifier()
    
    test_sentences = [
        "Arabamın motoru çalışmıyor",
        "Fren pedalı sertleşti",
        "Klima soğutmuyor",
        "Merhaba nasılsın",
        "Yemek tarifi ver",
        "Lastik basıncı kaç olmalı",
        "Vites zor giriyor",
        "Akü değişimi nasıl yapılır"
    ]
    
    print("\n" + "="*50)
    print("INTENT CLASSIFICATION TEST")
    print("="*50 + "\n")
    
    for sentence in test_sentences:
        intent, score, _ = classifier.classify(sentence)
        desc = classifier.get_intent_description(intent)
        print(f"📝 '{sentence}'")
        print(f"   ➡️ {desc} (skor: {score:.3f})")
        print()
