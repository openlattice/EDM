# EDM

jwt="*"
baseurl='http://localhost:8080'
gitsha='*'

python run.py --jwt=$jwt --baseurl=$baseurl --stage "PR" --gitsha=$gitsha
python run.py --jwt=$jwt --baseurl=$baseurl --stage "merge" --gitsha=$gitsha