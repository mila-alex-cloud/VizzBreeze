import os
import sys
import subprocess
from pathlib import Path

def main():
    """
    Entry point to automatically locate and launch the Streamlit visualization engine.
    """
    # Находим абсолютный путь к файлу app.py, который лежит в этой же папке пакета
    app_path = Path(__file__).parent / "app.py"
    
    if not app_path.exists():
        print(f"Error: Application core file not found at {app_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        # Автоматически вызываем 'streamlit run' из-под капота
        subprocess.run(["streamlit", "run", str(app_path)], check=True)
    except KeyboardInterrupt:
        print("\nDashboard execution terminated by user.")
    except Exception as e:
        print(f"Execution failed: {e}", file=sys.stderr)
        sys.exit(1)