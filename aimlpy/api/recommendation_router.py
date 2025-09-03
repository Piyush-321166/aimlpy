from fastapi import APIRouter
from aimlpy.entity.recommendation_reqres import GetRecommendationRequest, GetRecommendationResponse
from aimlpy.service.recommendation_service import RecommendationService
from aimlpy.entity.common import ErrorCode

router = APIRouter(prefix="/ml", tags=["Recommendation"])


@router.get("/recommend", response_model=GetRecommendationResponse)
async def get_recommendation(user_id: str, top_n: int = 10):
    try:
        req = GetRecommendationRequest(user_id=user_id, top_k=top_n)
        service = RecommendationService()
        result = service.get_recommendation(req)

        if not result:
            return GetRecommendationResponse(
                recommendations=[],
                error=False,
                error_code=None,
                message="No recommendations found",
            )

        return result
    except Exception as e:
        return GetRecommendationResponse(
            recommendations=[],
            error=True,
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=str(e),
        )


@router.get("/recommend/ai", response_model=GetRecommendationResponse)
async def get_ai_recommendation(user_id: str, top_n: int = 10):
    try:
        req = GetRecommendationRequest(user_id=user_id, top_k=top_n)
        service = RecommendationService()
        result = service.get_ai_recommendation(req)

        if not result:
            return GetRecommendationResponse(
                recommendations=[],
                error=False,
                error_code=None,
                message="No AI recommendations found",
            )

        return result
    except Exception as e:
        return GetRecommendationResponse(
            recommendations=[],
            error=True,
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=str(e),
        )

