"""
LangChain + Gemini API Client Module
Car expert ChatBot with LangChain integration.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List, Dict, Tuple
from intent_classifier import IntentClassifier

# Load environment variables
load_dotenv()


class CarExpertChatBot:
    """Car problems expert ChatBot with LangChain"""
    
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

    def __init__(self, model_name: str = None):
        # Get API key from environment variable
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        
        # API Keys
        self.api_key = os.getenv("GEMINI_API_KEY")
        # OpenAI key is checked during initialization if needed

        
        self.chat_history: List[Dict[str, str]] = []
        self.messages: List = []
        # Allow choosing model; fall back to default if not provided
        self.model_name = model_name or "gemini-2.5-flash"
        
        # Intent Classifier başlat
        try:
            self.intent_classifier = IntentClassifier()
        except Exception as e:
            print(f"Intent classifier yüklenemedi: {e}")
            self.intent_classifier = None
        
        self.last_detected_intent = None
        self.last_intent_score = 0.0
        
        self.initialize_llm()
    
    def initialize_llm(self):
        """Initialize LangChain with Gemini"""
        try:
            # Check which model is selected
            if self.model_name.startswith("gpt"):
                 # OpenAI Model
                openai_api_key = os.getenv("OPENAI_API_KEY")
                if not openai_api_key:
                    raise ValueError("OPENAI_API_KEY bulunamadı! Lütfen .env dosyasını kontrol edin.")
                
                self.llm = ChatOpenAI(
                    model=self.model_name,
                    openai_api_key=openai_api_key,
                    temperature=0.7
                )
            else:
                # Gemini Model
                if not self.api_key:
                    raise ValueError(
                        "GEMINI_API_KEY bulunamadı! Lütfen .env dosyası oluşturup "
                        "GEMINI_API_KEY=your_api_key_here şeklinde ekleyin."
                    )
                
                self.llm = ChatGoogleGenerativeAI(
                    model=self.model_name,
                    google_api_key=self.api_key,
                    temperature=0.7
                )
            
            # Add system message
            self.messages = [
                SystemMessage(content=self.SYSTEM_PROMPT)
            ]
            
            return True
        except Exception as e:
            print(f"LLM initialization error: {e}")
            return False

    def set_model(self, model_name: str) -> bool:
        """Change model and re-initialize the LLM."""
        self.model_name = model_name
        # reset messages to keep system prompt intact
        self.messages = [SystemMessage(content=self.SYSTEM_PROMPT)]
        return bool(self.initialize_llm())
    
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
    
    def get_response(self, user_message: str) -> Tuple[str, str, float]:
        """Generate response to user message using LangChain
        
        Returns:
            Tuple[str, str, float]: (yanıt, tespit_edilen_intent, güven_skoru)
        """
        
        # Intent Classification ile kategori tespiti
        detected_intent = "bilinmiyor"
        intent_score = 0.0
        
        if self.intent_classifier:
            detected_intent, intent_score, _ = self.intent_classifier.classify(user_message)
            self.last_detected_intent = detected_intent
            self.last_intent_score = intent_score
        
        # Kapsam dışı intent kontrolü (selamlama hariç)
        if detected_intent == "kapsam_disi" and intent_score > 0.15:
            return ("""🚗 Üzgünüm, ben sadece araba ve araç sorunları konusunda uzman bir asistanım.

Bu konuda size yardımcı olamıyorum. Arabanızla ilgili bir sorunuz varsa memnuniyetle yardımcı olurum!

**Örnek sorular:**
- Arabamın motoru çalışmıyor, ne yapmalıyım?
- Fren pedalı sertleşti, nedeni ne olabilir?
- Araç ısınıyor ama kalorifer çalışmıyor
- Vites geçerken ses geliyor
- Akü ne sıklıkla değiştirilmeli?""", detected_intent, intent_score)
        
        try:
            # Add user message to history
            self.messages.append(HumanMessage(content=user_message))
            
            # Get response from LangChain
            response = self.llm.invoke(self.messages)
            
            # Add AI response to history
            self.messages.append(AIMessage(content=response.content))
            
            # Add to simple history
            self.chat_history.append({
                "role": "user",
                "content": user_message
            })
            self.chat_history.append({
                "role": "assistant", 
                "content": response.content
            })
            
            return response.content, detected_intent, intent_score
            
        except Exception as e:
            return f"⚠️ Yanıt üretilirken bir hata oluştu: {str(e)}", detected_intent, intent_score
    
    def get_intent_description(self, intent: str) -> str:
        """Intent için açıklama döndürür"""
        if self.intent_classifier:
            return self.intent_classifier.get_intent_description(intent)
        return "❓ Bilinmeyen"
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
        self.messages = [
            SystemMessage(content=self.SYSTEM_PROMPT)
        ]
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Return chat history"""
        return self.chat_history
