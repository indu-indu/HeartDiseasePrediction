import json

with open("heart.ipynb", "r", encoding="utf-8") as f:
    notebook = json.load(f)

for i, cell in enumerate(notebook.get("cells", [])):
    if cell.get("cell_type") == "code":
        source = "".join(cell.get("source", []))
        print(f"--- Cell {i} ---")
        print(source)
