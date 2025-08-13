import os
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse

from langchain_openai import ChatOpenAI
from smart_query.data_retriever.data_commons_retriever import DataCommonsRetriever
from smart_query.data_retriever.energy_atlas_retriever import EnergyAtlasRetriever
from smart_query.data_retriever.ndpes_retriever import NDPESRetriever
from smart_query.data_retriever.wen_okn_retriever import WENOKNRetriever
from smart_query.data_system.data_system import LLMDataSystem
from smart_query.data_repo.dataframe_annotation import DataFrameAnnotation
from smart_query.utils.logger import get_logger

# Load environment variables                                                                                                                                           
load_dotenv()

# Create the main FastAPI application
app = FastAPI(
    title="Query Processing API",
    description="A simple API with a query processing endpoint",
    version="1.0.0"
)

# Create a router
router = APIRouter()

# Get logger
logger = get_logger(__name__)

# Setup LLM
OPENAI_KEY = os.getenv("OPENAI_KEY")  
if not OPENAI_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

llm = ChatOpenAI(model="gpt-4o", temperature=0, max_tokens=5000, api_key=OPENAI_KEY)

# Initialize the LLM based data system  
ds = LLMDataSystem(llm)
ds.add_dataframe_retriever(WENOKNRetriever("WEN-OKN Database", llm, join_query_compatible=True))
ds.add_dataframe_retriever(DataCommonsRetriever("Data Commons", llm))
ds.add_dataframe_retriever(EnergyAtlasRetriever("Energy Atlas", llm))
ds.add_text_retriever(NDPESRetriever("NDPES", llm))

@router.get("/query", include_in_schema=True)
async def process_query(query: str):
    """
    Process a query string and return a response.
    
    Args:
        query (str): The query string to process
        
    Returns:
        dict: A JSON response containing the processed query
    """
    try: 
        # Basic validation  
        if not query or query.strip() == "":
            raise HTTPException(status_code=400, detail="Query parameter cannot be empty")
        
        logger.info(f"Processing query: {query}")  
        
        # Remove all 5 minutes old dataframe annotations 
        if len(ds.data_repo.dataframe_annotations) > 10:
            ds.remove_annotations_older_than(60 * 5)

        dfa = ds.process_request(query)
        
        # Check if dfa and dfa.df exist before processing
        if dfa is None or dfa.df is None:
            raise HTTPException(status_code=404, detail="No data found for the query")
        
        # Handle potential JSON serialization issues
        try:
            result_json = dfa.df.reset_index(drop=True).to_json(orient='records')
        except Exception as json_error:
            logger.error(f"JSON serialization error: {json_error}")
            raise HTTPException(status_code=500, detail="Error serializing result data")
        
        logger.info(f"Successfully processed query: {query}")
        
        return {
            "query": query,
            "result": result_json,
            "status": "success"  
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error processing query '{query}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Include the router in the main app
app.include_router(router, prefix="/api/v1", tags=["Query Processing"])

# Run the application 
if __name__ == "__main__":  
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )
