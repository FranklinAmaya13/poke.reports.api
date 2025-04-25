from pydantic import BaseModel, Field
from typing import Optional

class PokeRequest(BaseModel):

    id: Optional[int] = Field(
        default=None,
        ge=1,
        description="ID de la peticion"
    )

    pokemon_type: Optional[str] = Field(
        default=None,
        description="Tipo de pokemon",
        pattern="^[a-z-Z0-9_]+$"
    )
    
    sample_size: Optional[int] = Field(
        default=None,
        gt=0,
        description="Numero maximo de registros"
    )

    url: Optional[str] = Field(
        default=None,
        description="URL de la peticion",
        pattern="^https?://[^\$]+$"
    )

    status: Optional[str] = Field(
        default=None,
        description="Estado de la peticion",
        pattern="^(sent|completed|failed|inprogress)"
    )