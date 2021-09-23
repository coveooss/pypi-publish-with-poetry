from pathlib import Path
from subprocess import check_output


if __name__ == "__main__":
    if not Path('pyproject.toml').exists():
        raise Exception(f"Cannot find a `pyproject.toml` file in the current folder: {Path().resolve()}")

    project_name, version = check_output(("poetry", "version")).strip().decode().split(' ')
    print(version)
