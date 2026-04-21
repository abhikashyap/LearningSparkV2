# PySpark Local Setup Guide

Environment configured for "Learning Spark 2nd Edition" with PySpark.

## ✓ What's Installed

- **Java 17** (via Homebrew)
- **PySpark 4.1.1** (in virtual env `~/.pyspark-env`)
- **Jupyter Notebook** (for interactive notebooks)
- **MLflow** (for experiment tracking)

## Quick Start

### Option 1: Start Jupyter Notebook
```bash
source ~/.pyspark-env/bin/activate
export JAVA_HOME=$(/opt/homebrew/bin/brew --prefix openjdk@17)
export PATH=$JAVA_HOME/bin:$PATH
jupyter notebook --no-browser --ip=127.0.0.1
```

Or use the setup script:
```bash
bash /Users/abhikashyap10/spark/LearningSparkV2/spark-notebook-setup.sh
```

Then open: **http://localhost:8888**

### Option 2: Run PySpark Examples from CLI
```bash
source ~/.pyspark-env/bin/activate
export JAVA_HOME=$(/opt/homebrew/bin/brew --prefix openjdk@17)
export PATH=$JAVA_HOME/bin:$PATH

cd chapter2/py/src
spark-submit mnmcount.py data/mnm_dataset.csv
```

## Permanent Shell Setup

Add to `~/.zshrc`:
```bash
# PySpark environment
export JAVA_HOME=$(/opt/homebrew/bin/brew --prefix openjdk@17)
export PATH=$JAVA_HOME/bin:$PATH
source ~/.pyspark-env/bin/activate
export SPARK_HOME=$(python -c "import pyspark; print(pyspark.__path__[0])" 2>/dev/null)
export PATH=$SPARK_HOME/bin:$PATH
```

Then reload:
```bash
source ~/.zshrc
```

## Verification

Test PySpark works:
```bash
python -c "from pyspark.sql import SparkSession; s = SparkSession.builder.getOrCreate(); print('✓ PySpark', s.version, 'ready')"
```

Test first example:
```bash
cd chapter2/py/src && spark-submit mnmcount.py data/mnm_dataset.csv
```

Expected output: M&M candies aggregated by state and color (California counts printed at end).

## Notebooks

**Import DBC notebook to Jupyter:**
1. Start Jupyter (see Quick Start)
2. Install `jupyter-databricks` to read DBC format: `pip install jupyter-databricks`
3. Or export notebooks from `notebooks/LearningSparkv2.dbc` to IPYNB format manually

**Alternative:** Use Databricks Community Edition or Azure Databricks for native DBC support.

## Running Spark Examples

**Python (no build step):**
```bash
spark-submit chapter2/py/src/mnmcount.py chapter2/py/src/data/mnm_dataset.csv
```

**Scala/Java (requires SBT build):**
```bash
cd chapter2/scala
sbt clean package
spark-submit --class main.scala.chapter2.MnMcount jars/main-scala-chapter2_2.12-1.0.jar data/mnm_dataset.csv
```

## Spark UI

Every `spark-submit` job opens a Spark UI at:
- **http://localhost:4040** (or next available port if 4040 busy)

Monitor: tasks, stages, executors, storage (cache), SQL queries, streaming.

## Troubleshooting

**Java not found:**
```bash
export JAVA_HOME=$(/opt/homebrew/bin/brew --prefix openjdk@17)
```

**PySpark import fails:**
Ensure virtual env is activated: `source ~/.pyspark-env/bin/activate`

**Port 8888 (Jupyter) already in use:**
```bash
jupyter notebook --no-browser --ip=127.0.0.1 --port 8889
```

**Can't read .dbc files in Jupyter:**
Use Databricks notebook viewer or convert to IPYNB manually. Or use Databricks Community Edition.

## Next Steps

Follow the learning plan in `/Users/abhikashyap10/.claude/plans/tidy-baking-pebble.md`.

Start with **Chapter 2** examples:
```bash
cd chapter2/py/src && spark-submit mnmcount.py data/mnm_dataset.csv
```

View Spark UI at http://localhost:4040 to understand DAG execution.
