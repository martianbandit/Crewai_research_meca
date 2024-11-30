import shutil
from pathlib import Path
import os

def cleanup_project():
    """Nettoie le projet des fichiers inutiles"""
    
    # Répertoire racine du projet
    root_dir = Path(__file__).parent
    
    # Liste des éléments à supprimer
    to_remove = [
        ".devcontainer",
        "examples",
        "__pycache__",
        "*.pyc",
        ".pytest_cache",
        "app/auth",  # Remplacé par l'authentification Streamlit native
        "data/sample_data.json"
    ]
    
    # Suppression des éléments
    for item in to_remove:
        if "*" in item:
            # Suppression des fichiers avec pattern
            for f in root_dir.rglob(item):
                try:
                    if f.is_file():
                        f.unlink()
                    elif f.is_dir():
                        shutil.rmtree(f)
                except Exception as e:
                    print(f"Erreur lors de la suppression de {f}: {str(e)}")
        else:
            # Suppression des éléments spécifiques
            path = root_dir / item
            if path.exists():
                try:
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
                except Exception as e:
                    print(f"Erreur lors de la suppression de {path}: {str(e)}")
    
    # Création des répertoires nécessaires
    directories = [
        "data/vector_store",
        "data/diagnostic_reports",
        "data/inspection_reports",
        "data/maintenance_plans",
        "data/memory"
    ]
    
    for directory in directories:
        dir_path = root_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("Nettoyage terminé avec succès!")

if __name__ == "__main__":
    cleanup_project()
