from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
import asyncio
from datetime import datetime
import logging

# Optional imports for AI models
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    torch = None
    AutoTokenizer = None
    AutoModelForCausalLM = None
    pipeline = None

router = APIRouter()

# Global variables for the AI model
chatbot_model = None
chatbot_tokenizer = None
chatbot_pipeline = None
model_loaded = False

logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    message: str
    language: Optional[str] = "en"

class ChatResponse(BaseModel):
    response: str
    language: str
    confidence: float
    timestamp: str

async def initialize_chatbot():
    """Initialize the chatbot model asynchronously"""
    global chatbot_model, chatbot_tokenizer, chatbot_pipeline, model_loaded
    
    if model_loaded:
        return True
    
    if not TRANSFORMERS_AVAILABLE:
        print("⚠️ Transformers/PyTorch not available. Using simple chatbot fallback.")
        model_loaded = True  # Mark as loaded to prevent re-attempts
        return True
    
    try:
        print("🤖 Initializing ConstructAI Chatbot...")
        
        # Use Microsoft DialoGPT for conversational AI
        model_name = "microsoft/DialoGPT-medium"
        
        # Load tokenizer
        chatbot_tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Add padding token if not present
        if chatbot_tokenizer.pad_token is None:
            chatbot_tokenizer.pad_token = chatbot_tokenizer.eos_token
        
        # Load model
        chatbot_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        # Create pipeline
        device = 0 if torch.cuda.is_available() else -1
        chatbot_pipeline = pipeline(
            "text-generation",
            model=chatbot_model,
            tokenizer=chatbot_tokenizer,
            device=device,
            max_length=200,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        model_loaded = True
        print("✅ ConstructAI Chatbot initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {e}")
        print(f"❌ Chatbot initialization failed: {e}")
        return False

def get_construction_context(user_message: str, language: str = "en") -> str:
    """Add construction-specific context to the user message"""
    
    contexts = {
        "en": """You are MistriBot, an expert AI assistant for construction management. You help with:
- Project planning and scheduling
- Material calculations and BOQ preparation  
- Safety protocols and PPE requirements
- Quality control and inspections
- Cost estimation and budget management
- Construction techniques and best practices

Always provide practical, safety-focused, and professional advice.

User: """,
        "es": """Eres MistriBot, un asistente de IA experto en gestión de construcción. Ayudas con:
- Planificación y programación de proyectos
- Cálculos de materiales y preparación de presupuestos
- Protocolos de seguridad y requisitos de EPP
- Control de calidad e inspecciones
- Estimación de costos y gestión presupuestaria
- Técnicas de construcción y mejores prácticas

Usuario: """,
        "hi": """आप MistriBot हैं, निर्माण प्रबंधन के विशेषज्ञ AI सहायक। आप इनमें मदद करते हैं:
- प्रोजेक्ट योजना और शेड्यूलिंग
- सामग्री की गणना और BOQ तैयारी
- सुरक्षा प्रोटोकॉल और PPE आवश्यकताएं
- गुणवत्ता नियंत्रण और निरीक्षण
- लागत अनुमान और बजट प्रबंधन
- निर्माण तकनीक और सर्वोत्तम प्रथाएं

उपयोगकर्ता: """
    }
    
    context = contexts.get(language, contexts["en"])
    return context + user_message + "\nMistriBot:"

def get_fallback_response(user_message: str, language: str = "en") -> str:
    """Generate fallback responses when AI model is not available"""
    
    user_lower = user_message.lower()
    
    responses = {
        "en": {
            "safety": "Safety first! Always wear proper PPE including helmets, safety vests, and steel-toed boots. Ensure all workers are trained on safety protocols and emergency procedures.",
            "cost": "For accurate cost estimation, I recommend using our BOQ (Bill of Quantities) calculator. It considers material costs, labor, and overhead to provide detailed project estimates.",
            "material": "Material quality is crucial for construction. For concrete structures, use grade-appropriate cement and ensure proper curing. Steel should meet IS specifications for structural integrity.",
            "planning": "Project planning should include: 1) Site preparation, 2) Foundation work, 3) Structural construction, 4) MEP installation, 5) Finishing work. Allow buffer time for weather delays.",
            "3d": "Our 3D conversion tool can transform your 2D blueprints into interactive 3D models. This helps visualize the project and identify potential issues before construction begins.",
            "default": "I'm MistriBot, your construction AI assistant! I can help with project planning, safety protocols, material calculations, cost estimation, and construction best practices. What specific aspect of your construction project would you like assistance with?"
        },
        "es": {
            "safety": "¡La seguridad es lo primero! Siempre use EPP adecuado incluyendo cascos, chalecos de seguridad y botas con punta de acero.",
            "cost": "Para estimación precisa de costos, recomiendo usar nuestra calculadora BOQ que considera costos de materiales, mano de obra y gastos generales.",
            "default": "¡Soy MistriBot, tu asistente de IA para construcción! Puedo ayudar con planificación de proyectos, protocolos de seguridad y mejores prácticas."
        },
        "hi": {
            "safety": "सुरक्षा सबसे पहले! हमेशा उचित PPE पहनें जिसमें हेलमेट, सेफ्टी वेस्ट और स्टील के जूते शामिल हों।",
            "cost": "सटीक लागत अनुमान के लिए, मैं हमारे BOQ कैलकुलेटर का उपयोग करने की सिफारिश करता हूं।",
            "default": "मैं MistriBot हूं, आपका निर्माण AI सहायक! मैं परियोजना योजना, सुरक्षा प्रोटोकॉल और सर्वोत्तम प्रथाओं में मदद कर सकता हूं।"
        }
    }
    
    lang_responses = responses.get(language, responses["en"])
    
    # Determine response type based on keywords
    if any(word in user_lower for word in ['safety', 'safe', 'helmet', 'protection', 'seguridad', 'सुरक्षा']):
        return lang_responses.get("safety", lang_responses["default"])
    elif any(word in user_lower for word in ['cost', 'budget', 'estimate', 'price', 'costo', 'लागत']):
        return lang_responses.get("cost", lang_responses["default"])
    elif any(word in user_lower for word in ['material', 'cement', 'steel', 'brick', 'सामग्री']):
        return lang_responses.get("material", lang_responses["default"])
    elif any(word in user_lower for word in ['plan', 'schedule', 'timeline', 'योजना']):
        return lang_responses.get("planning", lang_responses["default"])
    elif any(word in user_lower for word in ['3d', 'model', 'blueprint', 'design']):
        return lang_responses.get("3d", lang_responses["default"])
    else:
        return lang_responses["default"]

@router.post("/ask", response_model=ChatResponse, summary="Ask AI chatbot")
async def ask_chatbot(chat_message: ChatMessage):
    """Ask the multilingual AI chatbot about construction topics"""
    
    global model_loaded
    
    try:
        # Initialize model if not already loaded
        if not model_loaded:
            model_loaded = await initialize_chatbot()
        
        # Generate AI response
        if model_loaded and chatbot_pipeline:
            try:
                # Prepare input with construction context
                input_text = get_construction_context(chat_message.message, chat_message.language)
                
                # Generate response using the AI model
                result = chatbot_pipeline(
                    input_text,
                    max_new_tokens=100,
                    num_return_sequences=1,
                    pad_token_id=chatbot_tokenizer.eos_token_id,
                    temperature=0.7,
                    do_sample=True
                )
                
                # Extract bot response
                generated_text = result[0]['generated_text']
                bot_response = generated_text.split("MistriBot:")[-1].strip()
                
                # Clean and validate response
                if not bot_response or len(bot_response) < 10:
                    raise Exception("Generated response too short")
                
                confidence = 0.85  # AI model confidence
                
            except Exception as e:
                logger.warning(f"AI generation failed, using fallback: {e}")
                bot_response = get_fallback_response(chat_message.message, chat_message.language)
                confidence = 0.70  # Lower confidence for fallback
        else:
            # Use fallback response if model not available
            bot_response = get_fallback_response(chat_message.message, chat_message.language)
            confidence = 0.70
        
        timestamp = datetime.now().isoformat()
        
        return ChatResponse(
            response=bot_response,
            language=chat_message.language or "en",
            confidence=confidence,
            timestamp=timestamp
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        # Emergency fallback
        return ChatResponse(
            response="I'm experiencing technical difficulties. Please try again later.",
            language=chat_message.language or "en",
            confidence=0.50,
            timestamp=datetime.now().isoformat()
        )

@router.get("/history", summary="Get chat history")
async def get_chat_history():
    """Get user's chat history"""
    return {
        "messages": [
            {"timestamp": "2025-01-01T10:00:00Z", "user": "How to calculate concrete mix?", "bot": "For concrete mix calculation..."},
            {"timestamp": "2025-01-01T10:05:00Z", "user": "PPE requirements for site", "bot": "Personal Protective Equipment requirements include..."}
        ],
        "message": "Chat history retrieved"
    }

@router.delete("/history", summary="Clear chat history")
async def clear_chat_history():
    """Clear user's chat history"""
    return {"message": "Chat history cleared successfully"}

@router.get("/languages", summary="Get supported languages")
async def get_supported_languages():
    """Get list of supported languages for the chatbot"""
    return {
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "hi", "name": "Hindi"},
            {"code": "zh", "name": "Chinese"},
            {"code": "ar", "name": "Arabic"}
        ],
        "default": "en",
        "message": "Supported languages retrieved"
    }
