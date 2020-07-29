#!/usr/bin/python

import os, sys, re, json, shutil, multiprocessing
from subprocess import Popen, PIPE, STDOUT

stage_counter = 0

def which(program):
  for path in os.environ["PATH"].split(os.pathsep):
    exe_file = os.path.join(path, program)
    if os.path.exists(exe_file):
      return exe_file
  return None

def build():
  EMSCRIPTEN_ROOT = os.environ.get('EMSCRIPTEN')
  if not EMSCRIPTEN_ROOT:
    emcc = which('emcc')
    EMSCRIPTEN_ROOT = os.path.dirname(emcc)

  if not EMSCRIPTEN_ROOT:
    print "ERROR: EMSCRIPTEN_ROOT environment variable (which should be equal to emscripten's root dir) not found"
    sys.exit(1)

  sys.path.append(EMSCRIPTEN_ROOT)
  import tools.building as emscripten

# wasm = 'wasm' in sys.argv
  wasm = True;
  closure = 'closure' in sys.argv
  add_function_support = 'add_func' in sys.argv

  target = 'ammo.js' if not wasm else 'ammo.wasm.js'

  # Main

  try:

    bullet_libs = [os.path.join ( 'local-install', 'lib', 'libBullet2FileLoader.a' ),
				   os.path.join ( 'local-install', 'lib', 'libBullet3Collision.a' ),
				   os.path.join ( 'local-install', 'lib', 'libBullet3Common.a' ),
				   os.path.join ( 'local-install', 'lib', 'libBullet3Dynamics.a' ),
				   os.path.join ( 'local-install', 'lib', 'libBullet3Geometry.a' ),
				   os.path.join ( 'local-install', 'lib', 'libBullet3OpenCL_clew.a' ),
				   os.path.join ( 'local-install', 'lib', 'libBulletCollision.a' ),
				   os.path.join ( 'local-install', 'lib', 'libBulletDynamics.a' ),
				   os.path.join ( 'local-install', 'lib', 'libBulletInverseDynamics.a' ),
				   os.path.join ( 'local-install', 'lib', 'libBulletSoftBody.a' ),
				   os.path.join ( 'local-install', 'lib', 'libLinearMath.a' )];

    args = '-O3 --llvm-lto 1 -s NO_EXIT_RUNTIME=1 -s NO_FILESYSTEM=1 -s EXPORTED_RUNTIME_METHODS=["UTF8ToString"]'
    if add_function_support:
      args += ' -s RESERVED_FUNCTION_POINTERS=20 -s EXTRA_EXPORTED_RUNTIME_METHODS=["addFunction"]'
    if not wasm:
      args += ' -s WASM=0 -s AGGRESSIVE_VARIABLE_ELIMINATION=1 -s ELIMINATE_DUPLICATE_FUNCTIONS=1 -s SINGLE_FILE=1 -s LEGACY_VM_SUPPORT=1'
    else:
      args += ''' -s WASM=1 -s BINARYEN_IGNORE_IMPLICIT_TRAPS=1'''
    if closure:
      args += ' --closure 1 -s IGNORE_CLOSURE_COMPILER_ERRORS=1' # closure complains about the bullet Node class (Node is a DOM thing too)
    else:
      args += ' -s NO_DYNAMIC_EXECUTION=1'

    emcc_args = args.split(' ')

    emcc_args += ['-s', 'TOTAL_MEMORY=%d' % (64*1024*1024)] # default 64MB. Compile with ALLOW_MEMORY_GROWTH if you want a growable heap (slower though).
    #emcc_args += ['-s', 'ALLOW_MEMORY_GROWTH=1'] # resizable heap, with some amount of slowness

    emcc_args += '-s EXPORT_NAME="Ammo" -s MODULARIZE=1'.split(' ')

#   temp = os.path.join('..', '..', 'builds', target)
    temp = target;
    emscripten.emcc ( '-DNOTHING_WAKA_WAKA', 
                      emcc_args + ['glue.o'] + bullet_libs + ['--js-transform', 'python %s' % os.path.join('..', 'ammo-a', 'bundle.py')],
                      temp )

    assert os.path.exists(temp), 'Failed to create script code'

    wrapped = '''
  // This is ammo.js, a port of Bullet Physics to JavaScript. zlib licensed.
  ''' + open(temp).read()

    open(temp, 'w').write(wrapped)

  finally:
    print ( 'ok?' );

if __name__ == '__main__':
  build()

