import json
import logging

from fastapi import HTTPException
from models.PokeRequest import PokeRequest
from utils.database import execute_query_json
from utils.AzQueue import AzQueue
from utils.AzBlob import AzBlob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def update_pokemon_request( pokemon_request: PokeRequest) -> dict:
    try:
        query = " exec pokereports.update_poke_request ?, ?, ?"
        
        if not pokemon_request.url:
            pokemon_request.url = ""

        params = ( pokemon_request.id, pokemon_request.status, pokemon_request.url, )
        result = await execute_query_json( query, params, True )
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        logger.error( f"Error updating report request {e}" )
        raise HTTPException( status_code=500 , detail="Internal Server Error")

async def insert_pokemon_request( pokemon_request: PokeRequest) -> dict:
    try:
        query = " exec pokereports.created_poke_request ?, ? "
        params = ( pokemon_request.pokemon_type, pokemon_request.sample_size )
        result = await execute_query_json( query, params, True )
        result_dict = json.loads(result)
    

        await AzQueue().insert_message_on_queue( result )
        
        return result_dict
    except Exception as e:
        logger.error( f"Error selecting report request {e}" )
        raise HTTPException( status_code=500 , detail="Internal Server Error")
    
async def select_pokemon_request( id: int ) -> dict:
    try:
        query = " select * from pokereports.requests where id = ? "
        params = (id,)
        result = await execute_query_json( query, params )
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        logger.error( f"Error finding report request {e}" )
        raise HTTPException( status_code=500 , detail="Internal Server Error")

async def get_all_request() -> dict:
    query = """
        select 
            r.id as ReportId
            , s.description as Status
            , r.type as PokemonType
            , r.sample_size as sampleSize
            , r.url 
            , r.created 
            , r.updated
        from pokereports.requests r 
        inner join pokereports.status s 
        on r.id_status = s.id 
    """
    result = await execute_query_json( query )
    result_dict = json.loads(result)
    blob = AzBlob()
    for record in result_dict:
        id = record['ReportId']
        record['url'] = f"{record['url']}?{blob.generate_sas(id)}"
    return result_dict

async def delete_pokemon_request( id: int ) -> dict:
    try:
        params = (id,)
        result = await select_pokemon_request(id)

        if not result:
            raise HTTPException(status_code=404, detail=f"Registry with id {id} not found.")

        query_delete = " EXEC pokereports.delete_poke_request ? "
        result = await execute_query_json(query_delete, params, True)
        result_dict = json.loads(result)
        AzBlob().delete_csv(id)
        return result_dict

    except Exception as e:
        logger.error(f"Error deleting report request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
