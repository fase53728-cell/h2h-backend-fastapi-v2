from typing import List

from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models import League, Team, H2HAnalysis
from services.h2h_analyzer import (
    list_leagues,
    list_teams,
    analyze_h2h,
    create_league,
    save_team_csv,
)

app = FastAPI(
    title="H2H Predictor Backend",
    version="1.0.0",
    description="Backend FastAPI para análise H2H usando CSVs por time organizados por liga.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LeagueCreate(BaseModel):
    name: str


@app.get("/", tags=["status"])
def root():
    return {
        "message": "H2H Predictor API funcionando",
        "status": "online",
    }


@app.get("/leagues", response_model=List[League], tags=["ligas"])
def get_leagues():
    return list_leagues()


@app.post("/league", response_model=League, tags=["ligas"])
def post_league(payload: LeagueCreate):
    """Cria uma nova liga (pasta em data/leagues/{league_id})."""
    try:
        league = create_league(payload.name)
        return league
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar liga: {e}")


@app.get("/league/{league_id}/teams", response_model=List[Team], tags=["times"])
def get_teams(league_id: str):
    teams = list_teams(league_id)
    if not teams:
        raise HTTPException(status_code=404, detail="Liga não encontrada ou sem times")
    return teams


@app.post(
    "/league/{league_id}/upload-team",
    response_model=Team,
    tags=["times"],
)
async def upload_team_csv(
    league_id: str,
    file: UploadFile = File(..., description="Arquivo CSV do time"),
):
    """Importa o CSV de um time para uma liga existente."""
    try:
        content = await file.read()
        team = save_team_csv(league_id, file.filename, content)
        return team
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar CSV do time: {e}")


@app.get("/league/{league_id}/h2h", response_model=H2HAnalysis, tags=["h2h"])
def get_h2h(
    league_id: str,
    home: str = Query(..., description="Nome do time mandante (conforme nome do CSV)"),
    away: str = Query(..., description="Nome do time visitante (conforme nome do CSV)"),
):
    try:
        return analyze_h2h(league_id, home, away)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
