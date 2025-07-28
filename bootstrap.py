import os

structure = {
    "app.py": "",
    "requirements.txt": "",     
    "README.md": "# Driver Style Classifier\n\nDescribe your project here.",
    "kmeans.pkl": None,         
    ".streamlit": {
        "secrets.toml": "[general]\nOPENAI_API_KEY = \"sk-…\""
    },
    "utils": {
        "__init__.py": "",
        "features.py": ""
    }
}

def create(path, tree):
    for name, content in tree.items():
        full = os.path.join(path, name)
        if isinstance(content, dict):
            os.makedirs(full, exist_ok=True)
            create(full, content)
        else:
            with open(full, "w", encoding="utf-8") as f:
                if content:
                    f.write(content)

if __name__ == "__main__":
    root = os.getcwd()
    create(root, structure)
    print("Scaffold created in", root)
