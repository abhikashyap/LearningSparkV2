#!/bin/bash
# Activate PySpark virtual environment + start Jupyter notebook

# Set Java home
export JAVA_HOME=$(/opt/homebrew/bin/brew --prefix openjdk@17)
export PATH=$JAVA_HOME/bin:$PATH

# Activate venv
source ~/.pyspark-env/bin/activate

# Set Spark home
export SPARK_HOME=$(python -c "import pyspark; print(pyspark.__path__[0])")
export PATH=$SPARK_HOME/bin:$PATH

echo "✓ Java 17 configured"
echo "✓ JAVA_HOME: $JAVA_HOME"
echo "✓ PySpark environment activated"
echo "✓ SPARK_HOME: $SPARK_HOME"
echo ""
echo "Starting Jupyter Notebook..."
echo "Notebook will open at http://localhost:8888"
echo ""

# Start notebook in repo directory
cd /Users/abhikashyap10/spark/LearningSparkV2
jupyter notebook --no-browser --ip=127.0.0.1
