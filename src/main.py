import argparse
import sys
from pathlib import Path
from typing import Optional

# Import from core engine
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir.parent))  # Add src to path to allow imports
from core.engine import StoryEngine


def run(input_path: Path, domain: str, output_path: Optional[Path]) -> None:
    # 1. Setup Engine
    # Assumes structure:
    # project_root/
    #   src/main.py
    #   ontology/
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent.parent
    ontology_path = project_root / "ontology"
    
    engine = StoryEngine(ontology_path)
    
    # 2. Process
    text = input_path.read_text(encoding="utf-8", errors="ignore")
    result = engine.process(text, domain)
    
    # 3. Output
    print("\n".join(result["logs"]))
    
    if output_path:
        output_path.write_text(result["story"], encoding="utf-8")
        print(f"Generated story saved to: {output_path}")
    else:
        print(result["story"])


def main(argv: list[str]) -> int:
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
