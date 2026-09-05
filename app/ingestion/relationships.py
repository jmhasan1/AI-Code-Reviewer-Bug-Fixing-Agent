from enum import StrEnum

from pydantic import BaseModel


class RelationshipType(StrEnum):
    IMPORTS = "imports"
    CALLS = "calls"
    DEFINES = "defines"
    INHERITS_FROM = "inherits_from"


class CodeRelationship(BaseModel):
    repository_id: str
    source: str
    target: str
    relationship_type: RelationshipType
    file_path: str