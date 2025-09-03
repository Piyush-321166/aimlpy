from aimlpy.entity.recommendation_reqres import GetRecommendationRequest, GetRecommendationResponse
from aimlpy.entity.recommendation import Recommendation
from aimlpy.entity.common import ErrorCode


class RecommendationService:
    def get_recommendation(self, request: GetRecommendationRequest) -> GetRecommendationResponse:
        # existing code …
        pass

    def get_ai_recommendation(self, request: GetRecommendationRequest) -> GetRecommendationResponse:
        """Simple AI-powered recommendation stub."""
        try:
            user_id = request.user_id
            top_k = request.top_k or 10

            items = [f"item_{i}" for i in range(1, 101)]

            def score(uid: str, iid: str) -> float:
                key = f"{uid}:{iid}"
                return (abs(hash(key)) % 1000) / 1000.0

            recs = []
            for iid in items:
                s = score(user_id, iid)
                recs.append(
                    Recommendation(
                        user_id=str(user_id),
                        item_id=iid,
                        score=round(s, 4),
                        reason=f"Similar users with profile like {user_id} liked {iid}",
                    )
                )

            recs.sort(key=lambda r: r.score or 0.0, reverse=True)
            recs = recs[:top_k]

            return GetRecommendationResponse(recommendations=recs)
        except Exception as e:
            return GetRecommendationResponse(
                error=True,
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                message=str(e),
            )
