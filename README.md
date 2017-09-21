# Luigi Git
Uses Luigi to create a data pipeline.  
Creates a date.txt, time.txt and merges them into datetime.txt  
Automatically commits files into /results/{id=1}/

Usage:

```
pip install venv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
luigid --background --port=8082 --logdir=logs
python luigi_git.py DateTimeTask --id=1
```
