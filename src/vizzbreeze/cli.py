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
        # Create a copy of the current system environment variables
        env = os.environ.copy()
        # Set the max upload size via environment variables away from sys.argv
        env["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "2000"

        # Launch clean streamlit run WITHOUT extra arguments (just like before!)
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.maxUploadSize", "2000"
        ], env=env, check=True) # Pass our custom env mapping

    except KeyboardInterrupt:
        print("\nDashboard execution terminated by user.")
    except Exception as e:
        print(f"Execution failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

