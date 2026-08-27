import os
import sys
import subprocess
from pathlib import Path

import sys
import os
import subprocess
from pathlib import Path

def main():
    """
    Entry point to automatically locate and launch the Streamlit visualization engine.
    """
    app_path = Path(__file__).parent / "app.py"

    if not app_path.exists():
        print(f"Error: Application core file not found at {app_path}", file=sys.stderr)
        sys.exit(1)

    try:
        # Создаем копию текущего окружения системы
        env = os.environ.copy()
        # Незаметно для sys.argv передаем настройку размера файлов через окружение
        env["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "2000"

        # Запускаем чистый чистый streamlit run БЕЗ аргументов (как это было раньше!)
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path)
        ], env=env, check=True) # Передаем наше кастомное окружение env

    except KeyboardInterrupt:
        print("\nDashboard execution terminated by user.")
    except Exception as e:
        print(f"Execution failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

