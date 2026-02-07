from pathlib import Path
from typing import Dict, List, Any, Optional
import csv
import json

from .constants import CORE_ONTOLOGIES, OntologyCategory
from .schema import StorySoul, CharacterNode, SceneNode, EventNode, RelationshipEdge, ConceptRef
from .llm_client import LLMClient

class OntologyLoader:
    def __init__(self, ontology_root: Path):
        self.root = ontology_root
        self.concepts: Dict[str, Dict[str, str]] = {}
        self.categories: Dict[str, List[str]] = {c.value: [] for c in CORE_ONTOLOGIES}
        self._load_all()

    def _load_all(self):
        # Recursively load all csv files
        # In a real implementation, we would map specific CSVs to specific Categories
        # For now, we load everything and try to infer or just store flat
        for csv_file in self.root.glob("**/*.csv"):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'id' in row:
                        self.concepts[row['id']] = row
                        # Heuristic mapping for demo purposes
                        # Ideally, the CSV filename or a 'type' column maps to OntologyCategory
                        pass

    def get_concept(self, concept_id: str) -> Optional[Dict[str, str]]:
        return self.concepts.get(concept_id)
    
    def create_ref(self, cat: OntologyCategory, cid: str, label: str) -> ConceptRef:
        return ConceptRef(category=cat.value, id=cid, label=label)


class MemUClientStub:
    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    def store(self, key: str, value: Any) -> None:
        # Convert Pydantic models to dict
        if hasattr(value, "model_dump"):
             self._store[key] = value.model_dump()
        else:
             self._store[key] = value

    def retrieve(self, key: str) -> Any:
        return self._store.get(key)


class StoryEngine:
    def __init__(self, ontology_path: Path):
        self.ontology = OntologyLoader(ontology_path)
        self.memory = MemUClientStub()
        self.llm = LLMClient()

    def extract_soul(self, text: str) -> StorySoul:
        # 1. Use LLM to extract "The Soul" if available
        if self.llm.is_available():
            system_prompt = """
            あなたは物語構造解析のエキスパートです。
            入力された物語（小説や脚本）を解析し、独自の「LNA-ES Ontology」スキーマに基づいて
            JSON形式の構造データ（Story Soul）を抽出してください。
            
            出力は必ず以下のJSONスキーマに従ってください。
            特に、15種類のコアオントロジーカテゴリを意識して分類してください。
            
            Schema Structure:
            {
                "title": "物語のタイトル",
                "theme": {"category": "meta", "id": "MT_THEME", "label": "テーマ（例：信頼、復讐）"},
                "characters": [
                    {"id": "CH001", "name": "名前", "role": {"category": "character_function", "id": "CF_HERO", "label": "役割"}}
                ],
                "structure": [
                    {
                        "id": "SC01",
                        "context": {
                            "time": {"category": "temporal", "id": "TM_XXX", "label": "時間帯"},
                            "place": {"category": "spatial", "id": "SP_XXX", "label": "場所"},
                            "atmosphere": {"category": "natural", "id": "NT_XXX", "label": "雰囲気"}
                        },
                        "events": [
                            {
                                "actor_id": "CH001",
                                "action": {"category": "action", "id": "AC_XXX", "label": "行動"},
                                "emotion": {"category": "emotion", "id": "EM_XXX", "label": "感情"},
                                "motivation": {"category": "causality", "id": "CS_XXX", "label": "動機"}
                            }
                        ]
                    }
                ],
                "relationships": [
                    {"source_id": "CH001", "target_id": "CH002", "relation": {"category": "relationship", "id": "RL_XXX", "label": "関係性"}}
                ]
            }
            """
            try:
                data = self.llm.generate_json(system_prompt, f"以下の物語を解析してください:\n\n{text[:3000]}") # Limit text for token safety
                # Basic validation/repair could go here
                return StorySoul(**data)
            except Exception as e:
                print(f"LLM Extraction failed, falling back to mock: {e}")
        
        # Fallback Mock (Previous implementation)
        # Characters
        c_hero = CharacterNode(
            id="CH001", 
            name="メロス (Mock)",
            role=self.ontology.create_ref(OntologyCategory.CHARACTER_FUNCTION, "CF_HERO", "主人公")
        )
        c_villain = CharacterNode(
            id="CH002", 
            name="ディオニス (Mock)",
            role=self.ontology.create_ref(OntologyCategory.CHARACTER_FUNCTION, "CF_VILLAIN", "敵対者")
        )
        c_friend = CharacterNode(
            id="CH003", 
            name="セリヌンティウス (Mock)",
            role=self.ontology.create_ref(OntologyCategory.CHARACTER_FUNCTION, "CF_HELPER", "協力者")
        )

        # Scene 1: The Outrage
        s1 = SceneNode(
            id="SC01",
            context={
                "time": self.ontology.create_ref(OntologyCategory.TEMPORAL, "TM_DAY", "昼"),
                "place": self.ontology.create_ref(OntologyCategory.SPATIAL, "SP_CITY", "市街"),
                "atmosphere": self.ontology.create_ref(OntologyCategory.NATURAL, "NT_SILENCE", "静寂")
            },
            events=[
                EventNode(
                    actor_id="CH001",
                    action=self.ontology.create_ref(OntologyCategory.ACTION, "AC_OBSERVE", "目撃する"),
                    emotion=self.ontology.create_ref(OntologyCategory.EMOTION, "EM_ANGER", "激怒")
                ),
                EventNode(
                    actor_id="CH001",
                    action=self.ontology.create_ref(OntologyCategory.ACTION, "AC_DECIDE", "決意する"),
                    motivation=self.ontology.create_ref(OntologyCategory.CAUSALITY, "CS_JUSTICE", "正義感")
                )
            ]
        )

        # Relationships
        rels = [
            RelationshipEdge(
                source_id="CH001", target_id="CH002",
                relation=self.ontology.create_ref(OntologyCategory.RELATIONSHIP, "RL_HOSTILITY", "敵対")
            )
        ]

        soul = StorySoul(
            title="走れメロス (Mock)",
            theme=self.ontology.create_ref(OntologyCategory.META, "MT_TRUST", "信頼"),
            characters=[c_hero, c_villain, c_friend],
            structure=[s1],
            relationships=rels
        )
        
        return soul

    def contextual_forgetting(self, soul: StorySoul, domain: str) -> tuple[StorySoul, List[str]]:
        # "Forget" details that don't fit the target domain
        
        logs = []
        logs.append("--- [Contextual Forgetting Process] ---")
        logs.append(f">> Target Domain: {domain}")
        
        # If LLM is available, we could ask it what to forget/adapt
        # For now, we simulate the logic
        logs.append(">> Filtering Schema Nodes based on Domain Rules...")
        
        if domain == "school_drama":
             logs.append("   - Rule Applied: Replace 'Sword/Violence' with 'Social Conflict'")
             logs.append("   - Rule Applied: Scale down 'Death' to 'Social Exile/Expulsion'")
        elif domain == "jidai":
             logs.append("   - Rule Applied: Align Social Status to Edo Period (Samurai, Merchant)")
        
        logs.append(f"   - Retained Theme: {soul.theme.label if soul.theme else 'None'}")
        logs.append(f"   - Retained Characters: {[c.role.label for c in soul.characters]}")
        logs.append(f"   - Retained Scenes: {len(soul.structure)}")
        logs.append("---------------------------------------")
        
        return soul, logs

    def instantiate_story(self, soul: StorySoul, domain: str) -> str:
        # Reconstruct story based on domain using the Structured Soul
        
        if self.llm.is_available():
            system_prompt = f"""
            あなたはプロの小説家・シナリオライターです。
            提供された物語の構造データ（Story Soul）を元に、指定されたドメイン（世界観）で物語を再構築（リライト）してください。
            
            # 指示
            - ターゲットドメイン: {domain}
            - 元の構造（キャラクターの役割、感情の流れ、因果関係）は厳密に守ること。
            - 固有名詞や設定は、ターゲットドメインに合わせて適切に「翻訳」すること。
              例: 王様 -> 生徒会長 / 将軍 / 社長
              例: 処刑 -> 退学 / 切腹 / 解雇
            - 文体はドメインにふさわしいものにすること。
            - 長さは500〜1000文字程度で、物語のハイライトを描くこと。
            """
            
            user_prompt = f"""
            # Story Soul Data (JSON)
            {json.dumps(soul.model_dump(), ensure_ascii=False, indent=2)}
            
            # Output
            """
            
            try:
                return self.llm.generate_text(system_prompt, user_prompt)
            except Exception as e:
                print(f"LLM Generation failed: {e}")
                return f"Error generating story: {e}"

        # Fallback logic (Mock)
        if domain == "jidai":
            hero = soul.characters[0].name.replace("メロス", "若き剣士") 
            return f"（Mock出力: LLM未接続）\n【時代劇版】{hero}は走った..."
        else:
            return f"（Mock出力: LLM未接続）\n【学園版】{hero}は走った..."

    def process(self, text: str, domain: str) -> Dict[str, Any]:
        # 1. Extract Soul (Normalize to 15 Core Ontologies JSON)
        soul = self.extract_soul(text)
        
        # 2. Store in Memory
        self.memory.store("narrative_soul", soul)
        
        # 3. Contextual Forgetting & Filtering
        filtered_soul, logs = self.contextual_forgetting(soul, domain)
        
        # 4. Instantiate (The New Skin)
        story = self.instantiate_story(filtered_soul, domain)
        
        return {
            "story": story,
            "logs": logs,
            "graph": soul.model_dump() # Return JSON structure for visualization
        }
