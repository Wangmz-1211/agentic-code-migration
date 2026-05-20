import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Union

import yaml


def load_keywords(file_path: Union[str, Path]) -> List[str]:
    """Load keywords from a YAML file.

    Accepts a YAML list or a mapping; returns a list of strings.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Keywords file not found: {file_path}")
    with path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if data is None:
        return []
    if isinstance(data, list):
        return [str(x) for x in data]
    if isinstance(data, dict):
        # Accept mappings where values are the actual keywords
        return [str(v) for v in data.values()]
    return [str(data)]


def search_keywords_in_file(file_path: Union[str, Path], keywords: List[str], ignore_case: bool = False, use_regex: bool = False, whole_word: bool = False) -> dict:
    """Search for the presence of each keyword in the specified file.

    - `use_regex`: treat keywords as regex patterns
    - `whole_word`: wrap keywords in word boundaries when not using regex
    """
    results = {keyword: False for keyword in keywords}
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Target file not found: {file_path}")

    text = path.read_text(encoding='utf-8', errors='ignore')
    for keyword in keywords:
        if keyword == '':
            continue
        pattern = keyword
        flags = 0
        if ignore_case:
            flags = re.IGNORECASE
        if not use_regex:
            pattern = re.escape(keyword)
        if whole_word and not use_regex:
            pattern = r"\\b" + pattern + r"\\b"

        if re.search(pattern, text, flags=flags):
            results[keyword] = True
    return results


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Search for keywords inside a text file.')
    p.add_argument('target', help='Path to the target file to search')
    p.add_argument('-k', '--keywords', default='keywords.yaml', help='YAML file containing keywords (default: keywords.yaml)')
    p.add_argument('-i', '--ignore-case', action='store_true', help='Perform case-insensitive search')
    p.add_argument('-j', '--json', action='store_true', help='Output results as JSON')
    p.add_argument('--exit-code', action='store_true', help='Exit code 0 if any keyword found, 2 otherwise')
    p.add_argument('-r', '--recursive', action='store_true', help='If target is a directory, search files recursively')
    p.add_argument('-p', '--pattern', default='*', help='Glob pattern to match files when scanning directories (default: *)')
    p.add_argument('-e', '--ext', nargs='*', help='Filter by file extensions, e.g. -e .py .txt')
    p.add_argument('--regex', action='store_true', help='Treat keywords as regular expressions')
    p.add_argument('--word', action='store_true', help='Match whole words (adds word boundaries)')
    p.add_argument('-o', '--output', help='Write report to file (JSON if -j, otherwise text)')
    p.add_argument('--max-size', type=int, default=5_000_000, help='Skip files larger than this size in bytes (default 5MB)')
    return p


def scan_path(target: Union[str, Path], keywords: List[str], ignore_case: bool, use_regex: bool, whole_word: bool, recursive: bool, glob_pattern: str, exts: List[str], max_size: int) -> dict:
    """Scan a file or directory and return per-file keyword results and a summary."""
    target_path = Path(target)
    results = {}
    files_scanned = 0

    def should_include(p: Path) -> bool:
        if exts:
            return p.suffix in exts
        return True

    if target_path.is_file():
        if target_path.stat().st_size > max_size:
            return {'skipped': [str(target_path)], 'results': {}}
        results[str(target_path)] = search_keywords_in_file(target_path, keywords, ignore_case=ignore_case, use_regex=use_regex, whole_word=whole_word)
        files_scanned = 1
    else:
        pattern = glob_pattern
        iterator = target_path.rglob(pattern) if recursive else target_path.glob(pattern)
        for p in iterator:
            if not p.is_file():
                continue
            if p.stat().st_size > max_size:
                continue
            if not should_include(p):
                continue
            try:
                results[str(p)] = search_keywords_in_file(p, keywords, ignore_case=ignore_case, use_regex=use_regex, whole_word=whole_word)
                files_scanned += 1
            except Exception:
                continue

    # summary
    summary = {k: 0 for k in keywords}
    for file_res in results.values():
        for kw, found in file_res.items():
            if found:
                summary[kw] += 1

    return {'files_scanned': files_scanned, 'results': results, 'summary': summary}


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        keywords = load_keywords(args.keywords)
    except Exception as e:
        print(f"Error loading keywords: {e}", file=sys.stderr)
        sys.exit(2)

    if not keywords:
        print(f"No keywords found in {args.keywords}", file=sys.stderr)
        sys.exit(2)

    try:
        results = search_keywords_in_file(args.target, keywords, ignore_case=args.ignore_case)
    except Exception as e:
        print(f"Error searching target file: {e}", file=sys.stderr)
        sys.exit(2)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for keyword, found in results.items():
            print(f"{keyword}: {'Found' if found else 'Not found'}")

    if args.exit_code:
        if any(results.values()):
            sys.exit(0)
        else:
            sys.exit(2)


if __name__ == '__main__':
    main()