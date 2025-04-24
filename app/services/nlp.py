from typing import List, Dict, Any, Optional
import openai
from langdetect import detect
from ..core.config import settings
from ..models.schemas import QueryType, Product

class NLPService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    async def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process user query and return structured response."""
        try:
            # Detect language
            language = detect(query)
            
            # Prepare system message
            system_message = {
                "role": "system",
                "content": """You are an AI product recommendation assistant. 
                Analyze the user query and extract key information about their needs.
                Focus on understanding:
                1. Product category
                2. Key features/requirements
                3. Budget constraints
                4. Usage context
                Return a structured response with these details."""
            }
            
            # Prepare user message
            user_message = {
                "role": "user",
                "content": query
            }
            
            # Add context if available
            messages = [system_message]
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Previous context: {context}"
                })
            messages.append(user_message)
            
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse response
            analysis = response.choices[0].message.content
            
            # Determine query type
            query_type = self._determine_query_type(query, analysis)
            
            return {
                "analysis": analysis,
                "language": language,
                "query_type": query_type,
                "needs_clarification": self._needs_clarification(analysis)
            }
            
        except Exception as e:
            raise Exception(f"Error processing query: {str(e)}")

    def _determine_query_type(self, query: str, analysis: str) -> QueryType:
        """Determine the type of query based on content."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["best", "better", "vs", "compared"]):
            return QueryType.COMPARATIVE
        elif any(word in query_lower for word in ["with", "has", "need", "want"]):
            return QueryType.FEATURE_BASED
        else:
            return QueryType.SUBJECTIVE

    def _needs_clarification(self, analysis: str) -> bool:
        """Determine if the query needs clarification."""
        clarification_indicators = [
            "unclear",
            "ambiguous",
            "need more information",
            "specify",
            "clarify"
        ]
        return any(indicator in analysis.lower() for indicator in clarification_indicators)

    async def generate_clarification_question(self, analysis: str) -> str:
        """Generate a clarification question based on the analysis."""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Generate a single, clear question to clarify the user's needs."},
                    {"role": "user", "content": f"Based on this analysis: {analysis}"}
                ],
                temperature=0.7,
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating clarification: {str(e)}")

nlp_service = NLPService() 