import sys, subprocess, pathlib, os

try: import numpy as np
except:
  print("test.py requires numpy, install by running pip install numpy")
  exit(1)

def format_array(arr): return np.array2string(arr).replace('[[','').replace(' [','').replace(']','')

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} YOURPROGRAMHERE")
    exit(1)
  prog = pathlib.Path(sys.argv[1])
  if not prog.is_file():
    if prog.is_dir(): print(f"{prog} is a directory, not a file")
    else: print(f"no such file {prog} exists")
    exit(1)
  if not os.access(prog, os.X_OK):
    if prog.suffix in ['.c', '.cc', '.cpp', '.cxx', '.c++', '.cs', '.rs', '.zig', '.go', '.vb', '.f']:
      print(f"{prog} appears to be source code! compile first, and run test.py on the binary")
      exit(1)
    elif prog.suffix in ['.java', '.jar']:
      print(f"{prog} appears to be a java file. test.py does not currently work with java files")
      exit(1)
    print(f"{prog} is not executable. set the executable bit by running chmod +x {prog}")
    if prog.suffix == '.py':
      print(f"{prog} appears to be a python file. remember to add #!/usr/bin/env python to the top of your file")
    elif prog.suffix in ['.js', '.cjs', '.mjs']:
      print(f"{prog} appears to be a javascript file. remember to add #!/usr/bin/node to the top of your file")
    else: print(f"could not determine a shebang to suggest. if your code is interpreted, remember to add a shebang")
    exit(1)

  passed = True
  for N in [3, 4, 10, 16]:
    print(f"testing {N=:2} ... ", end="", flush=True)
    A = np.random.randint(10, size=(N,N))
    B = np.random.randint(10, size=(N,N))
    C = A@B
    test_C = subprocess.check_output(prog.resolve(), input=f"{N}\n{format_array(A)}\n{format_array(B)}\n".encode('utf-8'))
    if test_C.decode('utf-8').strip() == format_array(C).strip(): print('passed')
    else:
      print("failed")
      passed = False
  if passed: print("all tests passed")
  else: print("test failure detected")

