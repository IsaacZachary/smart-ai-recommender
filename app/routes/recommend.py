from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from ..models.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    Product,
    QueryType
)
from ..services.nlp import nlp_service
from ..services.products import product_service
from ..core.config import settings

router = APIRouter()

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get product recommendations based on user query.
    """
    try:
        # Process query with NLP
        nlp_result = await nlp_service.process_query(
            request.query,
            request.context
        )
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # If clarification is needed, return early
        if nlp_result["needs_clarification"]:
            clarification = await nlp_service.generate_clarification_question(
                nlp_result["analysis"]
            )
            return RecommendationResponse(
                clarification=clarification,
                products=[],
                session_id=session_id,
                query_type=nlp_result["query_type"]
            )
        
        # Search for products
        products = await product_service.search_products(
            request.query,
            {
                "language": nlp_result["language"],
                "query_type": nlp_result["query_type"]
            }
        )
        
        # Sort products by confidence score
        products.sort(key=lambda x: x.confidence_score, reverse=True)
        
        # Limit to top 5 products
        products = products[:5]
        
        return RecommendationResponse(
            clarification=None,
            products=products,
            session_id=session_id,
            query_type=nlp_result["query_type"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing recommendation: {str(e)}"
        )

@router.post("/clarify", response_model=RecommendationResponse)
async def clarify_recommendation(
    request: RecommendationRequest,
    session_id: str
):
    """
    Handle follow-up questions for clarification.
    """
    try:
        # Process clarification query
        nlp_result = await nlp_service.process_query(
            request.query,
            request.context
        )
        
        # Search for products with updated context
        products = await product_service.search_products(
            request.query,
            {
                "language": nlp_result["language"],
                "query_type": nlp_result["query_type"],
                "session_id": session_id
            }
        )
        
        # Sort and limit products
        products.sort(key=lambda x: x.confidence_score, reverse=True)
        products = products[:5]
        
        return RecommendationResponse(
            clarification=None,
            products=products,
            session_id=session_id,
            query_type=nlp_result["query_type"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing clarification: {str(e)}"
        ) 