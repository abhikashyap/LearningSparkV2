"""Convert Databricks .python notebook files to Jupyter .ipynb format."""

import json
import os
import glob

def replace_databricks_paths(source):
    """Replace Databricks dataset paths with local paths."""
    repo_root = "/Users/abhikashyap10/spark/LearningSparkV2"
    replacements = {
        '"/databricks-datasets/learning-spark-v2/': f'"{repo_root}/databricks-datasets/learning-spark-v2/',
        "'/databricks-datasets/learning-spark-v2/": f"'{repo_root}/databricks-datasets/learning-spark-v2/",
    }
    for old, new in replacements.items():
        source = source.replace(old, new)
    return source

def command_to_cell(cmd):
    source = cmd.get("command", "").strip()
    if not source:
        return None

    # Replace Databricks paths with local paths
    source = replace_databricks_paths(source)

    if source.startswith("%md"):
        text = source[3:].strip()
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": text.splitlines(keepends=True)
        }
    elif source.startswith("%sql"):
        code = "# SQL cell\n" + source[4:].strip()
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code.splitlines(keepends=True)
        }
    elif source.startswith("%"):
        # Other magic commands (%scala, %r, %sh, etc.) — keep as comment
        lines = source.splitlines()
        lines[0] = "# " + lines[0]
        source = "\n".join(lines)

    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True)
    }

def dbc_to_ipynb(dbc_path, output_path):
    with open(dbc_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Prepend SparkSession init cell for local Jupyter
    init_code = """from pyspark.sql import SparkSession

spark = SparkSession.builder \\
    .appName("LearningSparkV2") \\
    .master("local[*]") \\
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print(f"Spark {spark.version} ready")"""

    cells = [
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": init_code.splitlines(keepends=True)
        }
    ]

    for cmd in nb.get("commands", []):
        cell = command_to_cell(cmd)
        if cell:
            cells.append(cell)

    ipynb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (PySpark)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "cells": cells
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ipynb, f, indent=2)

    print(f"✓ {os.path.basename(dbc_path)} → {output_path}")

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(base, "dbc_content/Learning-Spark/Python")
    dst = os.path.join(base, "ipynb")

    pattern = os.path.join(src, "**/*.python")
    files = glob.glob(pattern, recursive=True)

    if not files:
        print(f"No .python files found in {src}")
        return

    for fp in sorted(files):
        rel = os.path.relpath(fp, src)
        out = os.path.join(dst, rel.replace(".python", ".ipynb"))
        try:
            dbc_to_ipynb(fp, out)
        except Exception as e:
            print(f"✗ {fp}: {e}")

    print(f"\n✓ Converted {len(files)} notebooks → {dst}/")

if __name__ == "__main__":
    main()
