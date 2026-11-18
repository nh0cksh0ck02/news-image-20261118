import logging
import os
import shutil
import sys
from pathlib import Path
from typing import List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("news-image-exporter")

def find_entry_file(candidate_dirs: List[Path]) -> Optional[Path]:
    for directory in candidate_dirs:
        candidate = directory / "entry.png"
        logger.debug(f"Checking candidate path: {candidate}")
        if candidate.is_file():
            logger.info(f"Discovered source entry image at: {candidate}")
            return candidate
    return None

def main():
    candidate_paths = [
        Path(__file__).resolve().parent,
        Path("/bot"),
        Path.cwd()
    ]

    source_file = find_entry_file(candidate_paths)

    if not source_file:
        logger.error("Failed to locate entry.png across all search locations.")
        sys.exit(1)

    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_dir = Path(output_dir_env)
    
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        logger.error(f"Cannot create output directory {output_dir}: {exc}")
        sys.exit(2)

    dest_file = output_dir / "entry.png"
    try:
        shutil.copy2(source_file, dest_file)
        file_size = dest_file.stat().st_size
        logger.info(f"Successfully copied entry.png to {dest_file} ({file_size:,} bytes)")
    except Exception as exc:
        logger.error(f"Error copying entry file to destination: {exc}")
        sys.exit(3)

if __name__ == "__main__":
    main()
