import logging
import time
from typing import Optional, List, Tuple
from openai import OpenAI
from rag_pipeline import RAGPipeline
from config import get_settings
from schemas import QueryCategory

logger = logging.getLogger(__name__)
settings = get_settings()


class LLMService:
    """Service for interacting with LLM and generating responses"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.rag_pipeline = RAGPipeline()
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
    
    def categorize_query(self, query: str) -> QueryCategory:
        """Categorize user query using LLM"""
        try:
            categories = [cat.value for cat in QueryCategory]
            
            prompt = f"""Categorize this query into one of: {', '.join(categories)}
            Query: {query}
            Category:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=10
            )
            
            category_text = response.choices[0].message.content.strip().lower()
            for cat in QueryCategory:
                if cat.value in category_text:
                    return cat
            
            return QueryCategory.OTHER
        except Exception as e:
            logger.error(f"Error categorizing query: {e}")
            return QueryCategory.OTHER
    
    def retrieve_context(self, query: str, k: int = 5) -> Tuple[List[str], List[str], List[float]]:
        """Retrieve relevant documents for query"""
        try:
            results = self.rag_pipeline.search(query, k=k)
            
            if not results:
                logger.warning(f"No relevant documents found for query: {query}")
                return [], [], []
            
            texts = [r[0] for r in results]
            sources = [r[2] for r in results]
            confidences = [r[1] for r in results]
            
            return texts, sources, confidences
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return [], [], []
    
    def generate_response(
        self,
        query: str,
        context_texts: List[str],
        school_config: Optional[dict] = None
    ) -> Tuple[str, float]:
        """Generate response using LLM with retrieved context"""
        try:
            start_time = time.time()
            
            # Build context string
            context = "\n\n".join([f"Document {i+1}:\n{text}" for i, text in enumerate(context_texts)])
            
            # Build system prompt
            system_prompt = self._build_system_prompt(school_config)
            
            # Build user message
            user_message = f"""Context Information:
{context}

User Query: {query}

Please provide a helpful and accurate response based on the context above. If the context doesn't contain relevant information, suggest contacting the school directly."""
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=self.temperature,
                max_tokens=500,
                top_p=0.95
            )
            
            response_text = response.choices[0].message.content
            processing_time = time.time() - start_time
            
            logger.info(f"Generated response in {processing_time:.2f}s")
            
            return response_text, processing_time
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error processing your query. Please try again.", 0.0
    
    def generate_full_response(
        self,
        query: str,
        school_config: Optional[dict] = None,
        k: int = 5
    ) -> dict:
        """Generate full response with context retrieval"""
        try:
            start_time = time.time()
            
            # Categorize query
            category = self.categorize_query(query)
            
            # Retrieve context
            context_texts, sources, confidences = self.retrieve_context(query, k=k)
            
            # Generate response
            response_text, gen_time = self.generate_response(query, context_texts, school_config)
            
            # Calculate metrics
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            total_time = time.time() - start_time
            
            return {
                "response": response_text,
                "category": category.value,
                "sources": list(set(sources)),  # Remove duplicates
                "confidence": min(avg_confidence, 1.0),
                "processing_time": total_time,
                "context_retrieved": len(context_texts) > 0
            }
        except Exception as e:
            logger.error(f"Error in generate_full_response: {e}")
            return {
                "response": "An error occurred while processing your query.",
                "category": "other",
                "sources": [],
                "confidence": 0.0,
                "processing_time": 0.0,
                "context_retrieved": False
            }
    
    def _build_system_prompt(self, school_config: Optional[dict] = None) -> str:
        """Build system prompt with school information"""
        base_prompt = """You are a helpful AI assistant for a school. Your role is to answer questions from parents and students about school policies, fees, schedules, and other important information.

Guidelines:
- Be friendly and professional
- Provide accurate information based on the context
- If uncertain, recommend contacting the school office directly
- Keep responses concise but informative
- Use simple language that parents and students can understand"""
        
        if school_config and "custom_prompt" in school_config:
            base_prompt += f"\n\nSchool-Specific Instructions:\n{school_config['custom_prompt']}"
        
        return base_prompt
    
    def add_training_document(self, file_path: str, doc_name: str, category: str = "general") -> bool:
        """Add document for RAG training"""
        return self.rag_pipeline.add_document(file_path, doc_name, category)
    
    def get_system_stats(self) -> dict:
        """Get system statistics"""
        return {
            "model": self.model,
            "vector_store": self.rag_pipeline.get_stats(),
            "temperature": self.temperature
        }
