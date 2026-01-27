from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import shutil
from pathlib import Path
from src.main import run_generator
import json

app = FastAPI(title="GPT-Md API", description="API para Geração de Propostas Técnicas")

# Configuração de CORS para permitir o frontend React/Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles

from api.utils import save_upload_files, sanitize_content
from src.ai_agent import AIAgent
from src.context_loader import ContextLoader
from src.models import Intent
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

UPLOAD_DIR = Path("input/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/output", StaticFiles(directory="output"), name="output")

@app.get("/")
async def root():
    return {"message": "GPT-Md API is running"}

@app.post("/analyze")
async def analyze_instruction(
    instruction: str = Form(...),
    files: List[UploadFile] = File(None)
):
    try:
        # 1. Salva arquivos
        saved_files = save_upload_files(files, UPLOAD_DIR)
        
        # 2. Carrega Contexto
        docs_content = ""
        for file_path in saved_files:
            loader = ContextLoader(docs_path=file_path)
            docs_content += loader.load_technical_docs()
            
        # 3. Análise IA (Stage 1)
        agent = AIAgent()
        intent = agent.interpret_instruction(instruction, docs_content)
        
        return intent.model_dump()

    except Exception as e:
        print(f"Error in /analyze: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_proposal(
    instruction: str = Form(...),
    sizing: Optional[str] = Form("standard"),
    contingency: Optional[str] = Form("standard"),
    term: Optional[int] = Form(30),
    output_mode: Optional[str] = Form("unified"),
    separate_opex: Optional[bool] = Form(False),
    debug: Optional[bool] = Form(False),
    files: List[UploadFile] = File(None)
):
    try:
        # Salva arquivos de upload temporariamente
        temp_files = []
        if files:
            for file in files:
                file_path = UPLOAD_DIR / file.filename
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                temp_files.append(str(file_path))

        # Parâmetros para o gerador
        params = {
            "instruction": instruction,
            "sizing": sizing,
            "contingency": contingency,
            "term": term,
            "output_mode": output_mode,
            "separate_opex": separate_opex,
            "debug": debug,
            "use_docs": temp_files
        }

        # Executa o gerador (refatorado em src/main.py)
        result = run_generator(params)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history():
    output_dir = Path("output")
    if not output_dir.exists():
        return []
    
    history = []
    # Lista pastas de output (timestamps)
    for folder in sorted(output_dir.iterdir(), reverse=True):
        if folder.is_dir():
            files = [f.name for f in folder.iterdir()]
            history.append({
                "timestamp": folder.name,
                "files": files
            })
    return history

from src.database import Database
from src.engines import LaborEngine, LogisticsEngine, MaterialEngine
from src.engines.opex_engine import OpexEngine
from src.engines.pricing_engine import PricingEngine
from src.models import ProposalData, LogisticsPlan, Intent, TopicMapping, ProposalData
from src.main import apply_margins, save_md, save_csv # Helper from main

@app.post("/plan-logistics")
async def plan_logistics(intent: Intent):
    try:
        agent = AIAgent()
        # Default Parameters
        origin = "Jundiaí - SP"
        destination = "Local do Cliente" # Frontend should ideally provide this or we extract from Intent
        # If intent has detailed_logistics, we might want to respect it or re-plan?
        # Let's assume this endpoint is to START the planning.
        
        duration_days = (intent.estimated_duration_weeks or 4) * 5
        team_size = intent.logistics_override.team_size if intent.logistics_override else 1
        
        # We need instruction text. intent doesn't strictly have 'instruction_text' raw field separate from 'project_motivation'
        # We can use project_motivation as context
        context = intent.project_motivation or "Projeto padrão"
        
        log_plan = agent.plan_logistics(
            origin=origin,
            destination=destination,
            instruction_text=context,
            team_size=max(1, team_size),
            duration_days=duration_days
        )
        return log_plan
    except Exception as e:
        print(f"Error in /plan-logistics: {str(e)}")
        # Fallback default plan
        return LogisticsPlan()

@app.post("/pricing")
async def calculate_pricing(intent: Intent):
    try:
        db = Database()
        # Initialize engines
        # Research engine is skipped here for speed/determinism unless explicit?
        # LaborEngine needs research_engine optional.
        # Let's skip heavy research engine for the interactive pricing to be fast.
        labor_engine = LaborEngine(db) 
        logistics_engine = LogisticsEngine(db)
        material_engine = MaterialEngine(db)
        
        proposal = ProposalData()
        
        # 1. Setup Topics
        for i, scope_item in enumerate(intent.scope_items):
            proposal.topics.append(TopicMapping(
                topic_id=f"T-{i+1:02d}",
                description=f"{scope_item.name} ({scope_item.detected_quantity} un - {scope_item.action_type})"
            ))
            
        requires_certification = any("fibra" in i.name.lower() or "cabeamento" in i.name.lower() for i in intent.scope_items)
        
        # 2. Run Engines
        material_engine.calculate_materials(intent, proposal)
        material_engine.calculate_services(proposal, intent, requires_certification)
        labor_engine.calculate_labor(intent, proposal, requires_certification)
        
        # Logistics requires detailed_logistics or override
        # Before calling pricing, frontend must have set detailed_logistics via /plan-logistics or manual input
        if intent.detailed_logistics:
             logistics_engine.calculate_logistics(intent, proposal)
        
        proposal.opex_data = OpexEngine.calculate_opex(proposal, intent.scope_items)
        
        # 3. Apply Margins
        # Term matches default 30 days unless passed. 
        # API inputs for pricing doesn't have 'term'. We can add it to Intent or hardcode 30 for now.
        apply_margins(proposal, term_days=30)
        
        return proposal
        
    except Exception as e:
        print(f"Error in /pricing: {str(e)}")
        # raise to let frontend know
        raise HTTPException(status_code=500, detail=str(e))

from src.engines import ProposalAssembler, LibraryAssembler
import time
from datetime import datetime

class RedactionRequest(BaseModel):
    intent: Intent
    proposal: ProposalData

class AssembleRequest(BaseModel):
    intent: Intent
    proposal: ProposalData
    text_blocks: Dict[str, str] = Field(default_factory=dict)

@app.post("/redaction")
async def generate_redaction(req: RedactionRequest):
    try:
        agent = AIAgent()
        
        # Summarize for AI
        tech_summary_for_ai = "\n".join([f"- {t.description}" for t in req.proposal.topics])
        proposal_summary_for_ai = f"Total Horas: {sum(i.hours for i in req.proposal.labor_table)}h | Total CAPEX: {format_br_currency(req.proposal.grand_total_venda)}"
        
        redaction = agent.compose_technical_redaction(
            intent_summary=req.intent.project_motivation or "N/A",
            tech_scope=tech_summary_for_ai,
            proposal_summary=proposal_summary_for_ai
        )
        return redaction
    except Exception as e:
        print(f"Error in /redaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/assemble")
async def assemble_proposal(req: AssembleRequest):
    try:
        # 1. Prepare Output Dir
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = OUTPUT_DIR / timestamp
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Setup Assembler
        template_dir = "templates/"
        library_path = Path("templates/library")
        if library_path.exists():
            proposal_assembler = LibraryAssembler(library_dir=str(library_path))
        else:
             from src.engines import ProposalAssemblerV2
             proposal_assembler = ProposalAssemblerV2(template_dir=str(Path(template_dir) / "v2"))
        
        # 3. Prepare Context
        extra_context = req.text_blocks
        
        # 4. Assemble
        # We need to filter public items for the proposal content?
        # api logic should match verify public_intent logic or just pass intent.
        public_intent = req.intent.model_copy(deep=True)
        public_intent.scope_items = [item for item in req.intent.scope_items if item.visibility == "public"]
        
        # Mock processing duration
        processing_duration = 0.0 
        
        proposal_outputs = proposal_assembler.assemble(
            req.proposal, public_intent, processing_time=processing_duration,
            extra_context=extra_context, output_mode=req.intent.output_mode or "unified", separate_opex=False
        )
        
        generated_files = []
        for filename, content in proposal_outputs.items():
            content = sanitize_content(content, req.intent.client_name)
            final_filename = filename.replace(".md", f"_{timestamp}.md")
            final_path = output_dir / final_filename
            final_path.write_text(content, encoding="utf-8")
            generated_files.append(str(final_path))
            
        # Save auxiliary files
        save_md(output_dir, f"MAT_{timestamp}.md", "Tabela de Materiais", req.proposal.hardware_table)
        save_md(output_dir, f"MOD_{timestamp}.md", "Tabela de Mão de Obra", req.proposal.labor_table)
        save_csv(output_dir, f"MAT_{timestamp}.csv", req.proposal.hardware_table)
        save_csv(output_dir, f"MOD_{timestamp}.csv", req.proposal.labor_table)
        
        return {
            "status": "success",
            "output_dir": str(output_dir),
            "files": generated_files
        }

    except Exception as e:
        print(f"Error in /assemble: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Importa e registra o router de Registros (Base CRUD)
from src.routers import registers
app.include_router(registers.router)
