# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Codebase Overview

Learning Spark V2 repo with examples from the "Learning Spark 2nd Edition" book. Multi-language examples across chapters.

**Structure:**
- `chapter2/`, `chapter3/`, `chapter6/`, `chapter7/`: Standalone applications (Scala, Java, Python)
- `chapter6/java/`: Only Java-based chapter (uses SBT like others)
- `notebooks/`: Databricks notebooks (DBC format) for all chapters
- `mlflow-project-example/`: MLflow training project
- `databricks-datasets/`: Reference datasets (flights, loans, CCTV videos)

**Languages in use:**
- Scala (chapters 2, 3, 7) - SBT build tool
- Java (chapter 6) - SBT build tool  
- Python (chapters 2, 3, 7) - spark-submit directly, no build step needed

## Building

**Build all JAR files (Scala/Java only):**
```bash
python build_jars.py
```
Runs in parallel (4 workers) on chapters 2, 3, 6, 7. Each chapter's SBT build executes as: `cd chapterX/{scala|java} && sbt clean package`

**Build single chapter:**
```bash
cd chapterX/scala  # or java for chapter6
sbt clean package
mkdir jars
cp target/scala-2.12/main-{scala|java}-chapterX_2.12-1.0.jar jars/
```

## Running Examples

**Scala/Java apps (after building):**
```bash
cd chapterX/scala  # (or java for chapter6)
spark-submit --class main.scala.chapterX.ClassName jars/main-scala-chapterX_2.12-1.0.jar <args>
```

Example for chapter 2:
```bash
cd chapter2/scala
spark-submit --class main.scala.chapter2.MnMcount jars/main-scala-chapter2_2.12-1.0.jar data/mnm_dataset.csv
```

**Python apps (no build needed):**
```bash
cd chapterX/py/src
spark-submit app_name.py <args>
```

Example for chapter 2:
```bash
cd chapter2/py/src
spark-submit mnmcount.py data/mnm_dataset.csv
```

**MLflow project:**
```bash
cd mlflow-project-example
mlflow run . -P file_path=data/sf-airbnb-clean.parquet -P max_depth=5 -P num_trees=100
```

## Test Files

Python tests exist in chapter directories (e.g., `chapter2/py/src/test_agg.py`). Run with pytest or spark-submit.

## Requirements

- Apache Spark 3.0.0-preview2+ (SBT dependencies pin this)
- Scala 2.12.10
- Python with PySpark
- MLflow (for mlflow-project-example)
- SBT for building Scala/Java

Ensure `$SPARK_HOME/bin` is in `$PATH` to run `spark-submit` directly.

## Key Files to Know

- `build.sbt`: Per-chapter Scala/Java build config with Spark dependency versions
- `build_jars.py`: Multi-threaded build orchestrator for all chapters
- Chapter READMEs: Specific build/run instructions (sometimes newer than this file)

For detailed chapter-specific guidance, refer to each chapter's README.md.
