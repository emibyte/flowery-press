# flowery-press
supposedly a static site generator

## Usage
For purposes of local testing use main.sh script which generates the html out of the provided markup and then spins up the python http server to serve it on localhost:8888
```
python3 src/main.py
cd public && python3 -m http.server 8888
```

For deployment use the build script which generates the webpage with a given basepath (in case of github pages the repo name)
```
python3 src/main.py <BASE_PATH>
```

All the tests in the project can be run via the test.sh script
```
python3 -m unittest discover -s src
```
