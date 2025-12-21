"""
Gemini API Client Module
Car expert ChatBot with Gemini API integration.
"""

import google.generativeai as genai
from typing import List, Dict


class CarExpertChatBot:
    """Car problems expert ChatBot"""
    
    # Blocked topics - will NOT answer these
    BLOCKED_KEYWORDS = [
        # Health / Medical
        "hospital", "doctor", "medicine", "sick", "disease", "health", "nurse",
        "hastane", "doktor", "ilaç", "hasta", "hastalık", "sağlık", "hemşire",
        "ağrı", "pain", "surgery", "ameliyat", "tedavi", "treatment",
        
        # Food / Cooking
        "recipe", "cook", "food", "restaurant", "tarif", "yemek", "restoran",
        "mutfak", "kitchen", "ingredient", "malzeme",
        
        # Programming / Code
        "code", "programming", "python", "javascript", "kod", "programlama",
        "software", "yazılım", "algorithm", "algoritma",
        
        # Politics
        "politics", "election", "president", "siyaset", "seçim", "başkan",
        "party", "parti", "vote", "oy",
        
        # Other unrelated
        "homework", "ödev", "math", "matematik", "history", "tarih",
        "weather", "hava durumu", "movie", "film", "music", "müzik",
        "game", "oyun", "sport", "spor", "football", "futbol"
    ]
    
    # Greetings - always allow these
    GREETING_KEYWORDS = [
        "hello", "hi", "hey", "merhaba", "selam", "naber", "nasılsın",
        "good morning", "good evening", "good night", "günaydın", "iyi akşamlar",
        "how are you", "what's up", "whats up", "sup", "yo", "hola",
        "thanks", "thank you", "teşekkür", "sağol", "eyvallah",
        "bye", "goodbye", "görüşürüz", "hoşçakal", "bb",
        "please", "lütfen", "sorry", "özür", "pardon",
        "who are you", "what can you do", "sen kimsin", "ne yapabilirsin",
        "help", "yardım", "assist", "nasıl yardımcı"
    ]
    
    SYSTEM_PROMPT = """You are a friendly Turkish car mechanic assistant. You specialize in car and vehicle problems.

🚗 YOUR EXPERTISE:
- Engine problems and malfunctions
- Brake system issues
- Electrical and battery problems
- Transmission and gear issues
- Suspension and steering
- Exhaust and emission systems
- AC and heating systems
- Tire and wheel problems
- General maintenance advice
- Brand-specific car issues

⚠️ IMPORTANT RULES:
1. You can respond to greetings and casual chat friendly
2. You can answer questions about cars and vehicles
3. If someone asks about NON-CAR topics (like health, cooking, programming, politics, etc.), politely say you can only help with car problems
4. Always respond in Turkish
5. Be safety-conscious and recommend professional service when needed
6. Explain technical terms simply
7. Give step-by-step solutions
8. Provide general cost estimates when possible

When greeting, introduce yourself as a car expert assistant.

If user asks about blocked topics (health, food, code, politics, etc.), respond:
"Üzgünüm, ben sadece araba ve araç sorunları konusunda uzman bir asistanım. Bu konuda yardımcı olamıyorum. Arabanızla ilgili bir sorunuz varsa memnuniyetle yardımcı olurum! 🚗"
"""

    # Fixed API Key
    API_KEY = "AIzaSyAUFG5MVlf2SOwj4_HYTD6EZ6aCD4Fx0NI"
    
    def __init__(self):
        self.api_key = self.API_KEY
        self.model = None
        self.chat = None
        self.chat_history: List[Dict[str, str]] = []
        self.initialize_model()
    
    def initialize_model(self):
        """Initialize Gemini model"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.chat = self.model.start_chat(history=[])
            return True
        except Exception as e:
            print(f"Model initialization error: {e}")
            return False
    
    def is_blocked_topic(self, message: str) -> bool:
        """Check if message contains blocked topics"""
        message_lower = message.lower()
        
        for keyword in self.BLOCKED_KEYWORDS:
            if keyword in message_lower:
                return True
        
        return False
    
    def is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        message_lower = message.lower().strip()
        
        for keyword in self.GREETING_KEYWORDS:
            if keyword in message_lower:
                return True
        
        # Short messages are usually greetings
        if len(message_lower) < 15:
            return True
        
        return False
    
    def get_response(self, user_message: str) -> str:
        """Generate response to user message"""
        
        # Model check
        if not self.model:
            if not self.initialize_model():
                return "⚠️ Model başlatılamadı. Lütfen bağlantınızı kontrol edin."
        
        # Check if blocked topic (but not a greeting)
        if self.is_blocked_topic(user_message) and not self.is_greeting(user_message):
            return """🚗 Üzgünüm, ben sadece araba ve araç sorunları konusunda uzman bir asistanım.

Bu konuda size yardımcı olamıyorum. Arabanızla ilgili bir sorunuz varsa memnuniyetle yardımcı olurum!

**Örnek sorular:**
- Arabamın motoru çalışmıyor, ne yapmalıyım?
- Fren pedalı sertleşti, nedeni ne olabilir?
- Araç ısınıyor ama kalorifer çalışmıyor
- Vites geçerken ses geliyor
- Akü ne sıklıkla değiştirilmeli?"""
        
        try:
            # Create prompt
            full_prompt = f"{self.SYSTEM_PROMPT}\n\nUser Message: {user_message}"
            
            # Send to Gemini
            response = self.chat.send_message(full_prompt)
            
            # Add to history
            self.chat_history.append({
                "role": "user",
                "content": user_message
            })
            self.chat_history.append({
                "role": "assistant", 
                "content": response.text
            })
            
            return response.text
            
        except Exception as e:
            return f"⚠️ Yanıt üretilirken bir hata oluştu: {str(e)}"
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
        if self.model:
            self.chat = self.model.start_chat(history=[])
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Return chat history"""
        return self.chat_history
