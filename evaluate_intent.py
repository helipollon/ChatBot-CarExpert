"""
Intent Classification Evaluation Module
Precision, Recall, F1 Score metrikleri ile değerlendirme yapar.
"""

import os
import random
from typing import Dict, List, Tuple
from collections import defaultdict
from intent_classifier import IntentClassifier


class IntentEvaluator:
    """Intent Classification değerlendirme sınıfı"""
    
    def __init__(self, classifier: IntentClassifier, test_ratio: float = 0.2):
        """
        Args:
            classifier: Eğitilmiş IntentClassifier
            test_ratio: Test seti oranı (varsayılan %20)
        """
        self.classifier = classifier
        self.test_ratio = test_ratio
        self.test_data: List[Tuple[str, str]] = []
        self.predictions: List[Tuple[str, str, str]] = []  # (text, actual, predicted)
        
    def prepare_test_data(self, test_file: str = "test_intents.txt"):
        """Test verisini ayrı dosyadan yükler"""
        
        # Önce ayrı test dosyasını dene
        if os.path.exists(test_file):
            self._load_from_file(test_file)
            print(f"✅ Ayrı test dosyasından {len(self.test_data)} örnek yüklendi: {test_file}")
        else:
            # Ayrı dosya yoksa eğitim verisinden ayır
            print(f"⚠️ {test_file} bulunamadı, eğitim verisinden ayırılıyor...")
            self._split_from_training("intents.txt")
    
    def _load_from_file(self, filepath: str):
        """Dosyadan test verisi yükler"""
        self.test_data = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '|' in line:
                    parts = line.split('|', 1)
                    if len(parts) == 2:
                        intent, text = parts
                        self.test_data.append((intent.strip().lower(), text.strip()))
    
    def _split_from_training(self, data_file: str):
        """Eğitim verisinden test seti ayırır (yedek yöntem)"""
        all_data: Dict[str, List[str]] = defaultdict(list)
        
        if not os.path.exists(data_file):
            print(f"❌ {data_file} bulunamadı!")
            return
        
        with open(data_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '|' in line:
                    parts = line.split('|', 1)
                    if len(parts) == 2:
                        intent, text = parts
                        all_data[intent.strip().lower()].append(text.strip())
        
        # Her kategoriden test_ratio kadar örnek ayır
        self.test_data = []
        for intent, texts in all_data.items():
            random.seed(42)  # Tekrarlanabilirlik için
            n_test = max(1, int(len(texts) * self.test_ratio))
            test_samples = random.sample(texts, min(n_test, len(texts)))
            for text in test_samples:
                self.test_data.append((intent, text))
        
        print(f"✅ {len(self.test_data)} test örneği hazırlandı.")
    
    def evaluate(self) -> Dict:
        """Değerlendirme yapar ve metrikleri hesaplar"""
        if not self.test_data:
            self.prepare_test_data()
        
        self.predictions = []
        
        # Her test örneği için tahmin yap
        for actual_intent, text in self.test_data:
            predicted_intent, score, _ = self.classifier.classify(text)
            self.predictions.append((text, actual_intent, predicted_intent))
        
        # Metrikleri hesapla
        return self._calculate_metrics()
    
    def _calculate_metrics(self) -> Dict:
        """Precision, Recall, F1 Score hesaplar"""
        # Tüm intent'leri topla
        all_intents = set()
        for _, actual, predicted in self.predictions:
            all_intents.add(actual)
            all_intents.add(predicted)
        
        # Her intent için TP, FP, FN hesapla
        metrics = {}
        
        for intent in all_intents:
            tp = 0  # True Positive
            fp = 0  # False Positive
            fn = 0  # False Negative
            
            for _, actual, predicted in self.predictions:
                if actual == intent and predicted == intent:
                    tp += 1
                elif actual != intent and predicted == intent:
                    fp += 1
                elif actual == intent and predicted != intent:
                    fn += 1
            
            # Precision = TP / (TP + FP)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            
            # Recall = TP / (TP + FN)
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            
            # F1 = 2 * (Precision * Recall) / (Precision + Recall)
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
            metrics[intent] = {
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'support': tp + fn  # Gerçek örneklerin sayısı
            }
        
        # Macro average hesapla
        macro_precision = sum(m['precision'] for m in metrics.values()) / len(metrics)
        macro_recall = sum(m['recall'] for m in metrics.values()) / len(metrics)
        macro_f1 = sum(m['f1_score'] for m in metrics.values()) / len(metrics)
        
        # Accuracy hesapla
        correct = sum(1 for _, actual, predicted in self.predictions if actual == predicted)
        accuracy = correct / len(self.predictions) if self.predictions else 0.0
        
        return {
            'per_class': metrics,
            'macro_avg': {
                'precision': macro_precision,
                'recall': macro_recall,
                'f1_score': macro_f1
            },
            'accuracy': accuracy,
            'total_samples': len(self.predictions)
        }
    
    def get_confusion_matrix(self) -> Dict[str, Dict[str, int]]:
        """Confusion matrix oluşturur"""
        if not self.predictions:
            self.evaluate()
        
        # Tüm intent'leri al
        all_intents = sorted(set(
            [p[1] for p in self.predictions] + [p[2] for p in self.predictions]
        ))
        
        # Confusion matrix
        matrix: Dict[str, Dict[str, int]] = {
            intent: {i: 0 for i in all_intents} for intent in all_intents
        }
        
        for _, actual, predicted in self.predictions:
            matrix[actual][predicted] += 1
        
        return matrix
    
    def print_report(self):
        """Detaylı değerlendirme raporu yazdırır"""
        results = self.evaluate()
        
        print("\n" + "="*70)
        print("📊 INTENT CLASSIFICATION DEĞERLENDİRME RAPORU")
        print("="*70)
        
        print(f"\n📈 Genel Metrikler:")
        print(f"   • Accuracy: {results['accuracy']:.2%}")
        print(f"   • Toplam Örnek: {results['total_samples']}")
        
        print(f"\n📊 Macro Average:")
        print(f"   • Precision: {results['macro_avg']['precision']:.2%}")
        print(f"   • Recall: {results['macro_avg']['recall']:.2%}")
        print(f"   • F1 Score: {results['macro_avg']['f1_score']:.2%}")
        
        print("\n" + "-"*70)
        print(f"{'Kategori':<20} {'Precision':>12} {'Recall':>12} {'F1 Score':>12} {'Destek':>10}")
        print("-"*70)
        
        for intent, metrics in sorted(results['per_class'].items()):
            print(f"{intent:<20} {metrics['precision']:>11.2%} {metrics['recall']:>11.2%} {metrics['f1_score']:>11.2%} {metrics['support']:>10}")
        
        print("-"*70)
        
        # Confusion matrix
        print("\n📋 Confusion Matrix (satırlar: gerçek, sütunlar: tahmin):")
        matrix = self.get_confusion_matrix()
        intents = sorted(matrix.keys())
        
        # Header
        print(f"\n{'':>15}", end="")
        for intent in intents:
            print(f"{intent[:8]:>10}", end="")
        print()
        
        # Rows
        for actual in intents:
            print(f"{actual[:14]:<15}", end="")
            for predicted in intents:
                count = matrix[actual][predicted]
                if count > 0:
                    print(f"{count:>10}", end="")
                else:
                    print(f"{'·':>10}", end="")
            print()
        
        print("\n" + "="*70)
    
    def get_misclassified(self, limit: int = 10) -> List[Tuple[str, str, str]]:
        """Yanlış sınıflandırılan örnekleri döndürür"""
        if not self.predictions:
            self.evaluate()
        
        misclassified = [
            (text, actual, predicted) 
            for text, actual, predicted in self.predictions 
            if actual != predicted
        ]
        
        return misclassified[:limit]
    
    def save_report(self, filename: str = "evaluation_report.txt"):
        """Değerlendirme raporunu dosyaya kaydeder"""
        import io
        import sys
        
        # Çıktıyı yakala
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        self.print_report()
        
        # Yanlış sınıflandırmaları ekle
        print("\n📛 YANLIŞ SINIFLANDIRILAN ÖRNEKLER:")
        print("-"*70)
        for text, actual, predicted in self.get_misclassified(20):
            print(f"Metin: {text[:50]}...")
            print(f"   Gerçek: {actual} → Tahmin: {predicted}")
            print()
        
        report = buffer.getvalue()
        sys.stdout = old_stdout
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Rapor kaydedildi: {filename}")
        return report


# Ana çalıştırma
if __name__ == "__main__":
    print("🔄 Intent Classifier yükleniyor...")
    classifier = IntentClassifier()
    
    print("📊 Değerlendirme başlıyor...")
    evaluator = IntentEvaluator(classifier, test_ratio=0.2)
    evaluator.print_report()
    
    # Raporu kaydet
    evaluator.save_report("evaluation_report.txt")
    
    # Yanlış sınıflandırmaları göster
    print("\n📛 Örnek yanlış sınıflandırmalar:")
    for text, actual, predicted in evaluator.get_misclassified(5):
        print(f"  • '{text[:40]}...'")
        print(f"    Gerçek: {actual} → Tahmin: {predicted}")
