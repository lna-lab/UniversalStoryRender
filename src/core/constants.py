from enum import Enum

class OntologyCategory(str, Enum):
    # Foundation Layer (5)
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    EMOTION = "emotion"
    SENSATION = "sensation"
    NATURAL = "natural"

    # Relational Layer (3)
    RELATIONSHIP = "relationship"
    CAUSALITY = "causality"
    ACTION = "action"

    # Structural Layer (2)
    NARRATIVE_STRUCTURE = "narrative_structure"
    CHARACTER_FUNCTION = "character_function"

    # Cultural/Advanced/Meta (5)
    DISCOURSE_STRUCTURE = "discourse_structure"
    INDIRECT_EMOTION = "indirect_emotion"
    STYLE_FORMULA = "style_formula"
    FOOD_CULTURE = "food_culture"
    META = "meta"

# The chosen 15 Ontologies
CORE_ONTOLOGIES = [
    OntologyCategory.TEMPORAL,
    OntologyCategory.SPATIAL,
    OntologyCategory.EMOTION,
    OntologyCategory.SENSATION,
    OntologyCategory.NATURAL,
    OntologyCategory.RELATIONSHIP,
    OntologyCategory.CAUSALITY,
    OntologyCategory.ACTION,
    OntologyCategory.NARRATIVE_STRUCTURE,
    OntologyCategory.CHARACTER_FUNCTION,
    OntologyCategory.DISCOURSE_STRUCTURE,
    OntologyCategory.INDIRECT_EMOTION,
    OntologyCategory.STYLE_FORMULA,
    OntologyCategory.FOOD_CULTURE,
    OntologyCategory.META,
]
