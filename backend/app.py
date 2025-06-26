"""
app.py – FastAPI entrypoint for Math Word Problem Generator

Security Level: ★★★☆☆ (3/5)  
- All external inputs validated by Pydantic models.  
- CORS origins can be restricted via ALLOWED_ORIGINS list.  
- No file I/O or eval; runtime injectionリスク低。  
Evidence Strength: ★★★☆☆ (3/5)  
- 実装は FastAPI 公式ドキュメントに準拠。  
- 追加のペネトレーションテストと SCA 推奨。
"""

from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .generator import generate_problems






# -----------------------------------------------------------------------------
# Pydantic Schemas
# -----------------------------------------------------------------------------
class GenerateRequest(BaseModel):
    """API 受信用スキーマ：学年と難易度を検証する"""
    grade: int = Field(..., ge=1, le=12, description="1–12 = 小1〜高3")
    difficulty: int = Field(..., ge=1, le=5, description="難易度 1 (易) 〜 5 (難)")


class Problem(BaseModel):
    """単一の文章問題とヒントを表すレスポンス要素"""
    id: str
    question: str
    hints: List[str]


class GenerateResponse(BaseModel):
    """問題セットをレスポンスとして返す"""
    problems: List[Problem]


# -----------------------------------------------------------------------------
# FastAPI インスタンス生成
# -----------------------------------------------------------------------------
def create_app() -> FastAPI:
    """FastAPI アプリを生成し、CORS 等のミドルウェアを設定する"""
    app = FastAPI(
        title="Math Word Problem Generator API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS 設定：必要に応じてドメインを限定する
    ALLOWED_ORIGINS = ["http://localhost:5500", "https://example.com", "http://localhost:8000", "http://127.0.0.1:8000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["POST"],
        allow_headers=["*"],
    )

    # ルーティング設定
    register_routes(app)
    return app


# -----------------------------------------------------------------------------
# Route Definitions
# -----------------------------------------------------------------------------
def register_routes(app: FastAPI) -> None:
    """エンドポイントをアプリに登録する"""

    @app.get("/health", summary="ヘルスチェック", tags=["Utility"])
    async def health() -> dict:
        """稼働確認用エンドポイント"""
        return {"status": "ok"}

    @app.post(
        "/generate",
        response_model=GenerateResponse,
        summary="文章問題生成",
        tags=["Generator"],
    )
    async def generate(req: GenerateRequest) -> GenerateResponse:
        """
        学年・難易度に基づいて文章問題を生成し返却する
        - 学年 1–6: 小学生、7–9: 中学生、10–12: 高校生
        - 問題数は学年区分で自動調整
        """
        try:
            problems = generate_problems(req.grade, req.difficulty)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        return GenerateResponse(problems=problems)


# -----------------------------------------------------------------------------
# ASGI callable
# -----------------------------------------------------------------------------
app = create_app()
