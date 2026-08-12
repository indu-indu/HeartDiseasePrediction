import json

try:
    with open("heart2.ipynb", "r", encoding="utf-8") as f:
        notebook = json.load(f)
    print("Notebook downloaded successfully.")
    for i, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") == "code":
            source = "".join(cell.get("source", []))
            print(f"--- Cell {i} ---")
            print(source)
except Exception as e:
    print(e)
