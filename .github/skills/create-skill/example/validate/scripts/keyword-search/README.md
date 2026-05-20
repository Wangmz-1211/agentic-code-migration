
Usage
-----

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Basic usage (single file):

```bash
python main.py target.txt -k keywords.yaml
```

Scan a directory recursively, only `.py` and `.md` files, output JSON report:

```bash
python main.py path/to/project -k keywords.yaml -r -e .py .md -j -o report.json
```

Options (high level):
- `-i/--ignore-case`: case-insensitive search
- `-j/--json`: output results as JSON
- `-r/--recursive`: scan directories recursively
- `-p/--pattern`: glob pattern when scanning directories (default `*`)
- `-e/--ext`: filter by file extensions, e.g. `-e .py .txt`
- `--regex`: treat keywords as regular expressions
- `--word`: match whole words (adds word boundaries)
- `-o/--output`: write report to a file (JSON when used with `-j`)
- `--exit-code`: exit 0 if any keyword found, exit 2 otherwise

Example `keywords.yaml`:

```yaml
- TODO
- FIXME
- IMPORTANT
```

Tips:
- Use `--regex` for advanced patterns (be cautious with untrusted regexes).
- Increase `--max-size` if you need to scan very large files.
