conda activate videorag
rm -rf videorag-workdir
mkdir -p videorag-workdir
python -u insert.py > videorag-workdir/insert.log 
python -u query.py > videorag-workdir/query.log