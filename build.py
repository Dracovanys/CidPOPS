import os

root = os.path.dirname(os.path.abspath(__file__))

files_toBuild = ['main', 'src\\setup']

for script in files_toBuild:
    _script = []
    with open(f'{root}\\{script}.py', 'r') as file:
        for line in file.readlines():
            if line.find('# Build ') != -1:
                line = line.replace('# Build ', '')
            _script.append(line)
    with open(f'{script}_toBuild.py', 'w') as file:
        for line in _script:
            file.write(line)