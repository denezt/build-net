import pandas as pd
from pathlib import Path
from .models import ProjectMeta
import yaml

def process_metadata(input_dir: str, output_dir: str) -> pd.DataFrame:
    """Process directory of metadata files"""
    results = []

    for path in Path(input_dir).glob("*.yaml"):
        try:
            meta = ProjectMeta.from_yaml(str(path))
            result = {
                "file": path.name,
                "status": "valid",
                "project": meta.name,
                "contributors": len(meta.contributors)
            }
            save_processed(output_dir, meta)
        except Exception as e:
            result = {"file": path.name, "status": f"invalid: {str(e)}"}

        results.append(result)

    return pd.DataFrame(results)

def save_processed(output_dir: str, meta: ProjectMeta):
    """Save validated metadata"""
    path = Path(output_dir) / f"{meta.name}.json"
    path.parent.mkdir(exist_ok=True)
    with open(path, "w") as f:
        f.write(meta.model_dump_json(indent=2))
