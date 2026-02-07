import argparse
import sys
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional


class OntologyLoader:
    def __init__(self, ontology_root: Path):
        self.root = ontology_root
        self.concepts: Dict[str, Dict[str, str]] = {}
        self._load_all()

    def _load_all(self):
        # Recursively load all csv files
        for csv_file in self.root.glob("**/*.csv"):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'id' in row:
                        self.concepts[row['id']] = row

    def get_concept(self, concept_id: str) -> Optional[Dict[str, str]]:
        return self.concepts.get(concept_id)


class MemUClientStub:
    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    def store(self, key: str, value: Any) -> None:
        self._store[key] = value

    def retrieve(self, key: str) -> Any:
        return self._store.get(key)


def normalize_to_graph(text: str, ontology: OntologyLoader) -> Dict[str, Any]:
    # In a real system, this would use LLM to map text to ontology IDs
    # Here we simulate the extraction of "The Soul"
    
    # 1. Narrative Structure (Level 1 Memory)
    narrative_graph = {
        "nodes": [
            {"id": "CH001", "type": "character", "role": "hero"},  # Melos
            {"id": "CH002", "type": "character", "role": "villain"}, # King
            {"id": "CH003", "type": "character", "role": "friend"}, # Selinuntius
        ],
        "edges": [
            {"source": "CH001", "target": "CH002", "relation": "RL004", "label": "hostility"},
            {"source": "CH001", "target": "CH003", "relation": "RL001", "label": "friendship"},
        ],
        "emotional_arc": [
            "EM001", # Anger (激怒)
            "EM002", # Determination (決意)
            "EM003", # Anxiety (不安)
            "EM004", # Exhaustion (疲労)
            "EM005", # Joy (感動)
        ]
    }
    return narrative_graph


def contextual_forgetting(graph: Dict[str, Any], domain: str) -> Dict[str, Any]:
    # "Forget" details that don't fit the target domain
    # In this demo, the graph is already abstract, so we just log what we are ignoring
    
    print("--- [Contextual Forgetting Process] ---")
    print(">> Forgetting Source Domain Elements...")
    print("   - Ignoring: 'Syracuse' (Location)")
    print("   - Ignoring: 'Dionysus' (Proper Name)")
    print("   - Ignoring: 'Crucifixion' (Cultural Context)")
    print(">> Retaining Ontology Structure:")
    print(f"   - Hero: {graph['nodes'][0]['id']}")
    print(f"   - Emotion Arc: {graph['emotional_arc']}")
    print("---------------------------------------")
    
    return graph


def instantiate_story(graph: Dict[str, Any], domain: str, ontology: OntologyLoader) -> str:
    # Reconstruct story based on domain
    
    # Load domain specific vocabulary
    style_id = "SF001" if domain == "jidai" else "SF002"
    style = ontology.get_concept(style_id)
    
    emotions = [ontology.get_concept(eid)['concept'] for eid in graph['emotional_arc'] if ontology.get_concept(eid)]
    
    if domain == "jidai":
        # Mapping to Jidai Geki
        hero = "若き剣士"
        friend = "茶屋の店主"
        villain = "悪徳家老"
        setting = "江戸の城下町"
        return f"""【時代劇版 走れメロス】
舞台は{setting}。
{hero}（CH001）は、{villain}（CH002）の非道に触れ、{emotions[0]}（EM001）を覚えた。
友である{friend}（CH003）を人質に残し、{hero}は走り出す。
道中、{emotions[2]}（EM003）や{emotions[3]}（EM004）に襲われるも、{emotions[1]}（EM002）を胸に刻む。
ついに{villain}の元へ戻り、約束を果たした時、城下に{emotions[4]}（EM005）が広がった。"""
    
    else:
        # Mapping to School Youth
        hero = "陸上部のエース"
        friend = "新聞部の親友"
        villain = "冷徹な生徒会長"
        setting = "放課後の教室"
        return f"""【学園青春版 走れメロス】
舞台は{setting}。
{hero}（CH001）は、{villain}（CH002）の理不尽な決定に、{emotions[0]}（EM001）を感じていた。
廃部をかけたタイムリミット。{friend}（CH003）が身代わりとなる。
グラウンドを走る{hero}。襲いかかる{emotions[2]}（EM003）と{emotions[3]}（EM004）。
しかし{emotions[1]}（EM002）だけが彼を突き動かす。
ゴールテープを切った瞬間、{emotions[4]}（EM005）の涙が溢れ出した。"""


def run(input_path: Path, domain: str, output_path: Optional[Path]) -> None:
    # 1. Setup Ontology
    # Use relative path from this script location
    # Assumes structure:
    # project_root/
    #   src/main.py
    #   ontology/
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent
    ontology_path = project_root / "ontology"
    
    ontology = OntologyLoader(ontology_path)
    
    # 2. Normalize & Extract (The Soul)
    text = input_path.read_text(encoding="utf-8", errors="ignore")
    graph = normalize_to_graph(text, ontology)
    
    # 3. Store in Memory
    client = MemUClientStub()
    client.store("narrative_soul", graph)
    
    # 4. Contextual Forgetting
    filtered_graph = contextual_forgetting(graph, domain)
    
    # 5. Instantiate (The New Skin)
    story = instantiate_story(filtered_graph, domain, ontology)
    
    if output_path:
        output_path.write_text(story, encoding="utf-8")
        print(f"Generated story saved to: {output_path}")
    else:
        print(story)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(prog="memory_rag_demo", add_help=True)
    parser.add_argument("--input", required=True, help="入力テキストファイルのパス")
    parser.add_argument("--domain", choices=["jidai", "時代劇", "gakuen", "学園青春"], default="gakuen", help="変換ドメイン")
    parser.add_argument("--output", help="生成物語の出力ファイルパス")
    args = parser.parse_args(argv)
    in_path = Path(args.input)
    if not in_path.exists():
        print("入力ファイルが見つかりません", file=sys.stderr)
        return 1
    out_path = Path(args.output) if args.output else None
    domain = "jidai" if args.domain in {"jidai", "時代劇"} else "gakuen"
    run(in_path, domain, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
