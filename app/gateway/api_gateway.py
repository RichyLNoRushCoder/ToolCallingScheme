from fastapi import APIRouter, Depends, HTTPException

from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.analysis_service import AnalysisService
from app.utils.errors import AppError

router = APIRouter(prefix="/v1", tags=["analysis"])


def get_analysis_service() -> AnalysisService:
    from app.main import analysis_service

    return analysis_service


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    req: AnalyzeRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalyzeResponse:
    try:
        return await service.analyze(req)
    except AppError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"unexpected error: {exc}") from exc
