from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Represents a reference to an Ontology Concept
class ConceptRef(BaseModel):
    category: str  # One of the 15 categories
    id: str        # Ontology ID (e.g., EM001)
    label: str     # Human readable label (e.g., 激怒)
    value: Optional[Any] = None # Specific value if needed

# 1. Structural Layer: Character
class CharacterNode(BaseModel):
    id: str
    role: ConceptRef # CharacterFunction (e.g., Hero)
    archetype: Optional[ConceptRef] = None
    name: str

# 2. Structural Layer: Scene/Event
class EventNode(BaseModel):
    actor_id: str
    action: ConceptRef # Action
    target_id: Optional[str] = None
    emotion: Optional[ConceptRef] = None # Emotion
    motivation: Optional[ConceptRef] = None # Causality
    sensory_detail: Optional[ConceptRef] = None # Sensation

class SceneNode(BaseModel):
    id: str
    context: Dict[str, ConceptRef] = Field(
        default_factory=dict,
        description="Temporal, Spatial, Natural, Atmosphere"
    )
    events: List[EventNode] = []

# 3. Relational Layer
class RelationshipEdge(BaseModel):
    source_id: str
    target_id: str
    relation: ConceptRef # Relationship
    strength: float = 1.0

# Root Schema: The Soul
class StorySoul(BaseModel):
    title: str
    theme: Optional[ConceptRef] = None # Meta
    characters: List[CharacterNode]
    structure: List[SceneNode] # NarrativeStructure (Chronological)
    relationships: List[RelationshipEdge]
    
    # Metadata
    schema_version: str = "1.0"
    ontology_subset: str = "core_15"
