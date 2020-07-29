#!/usr/bin/python

import os, sys, re, json, shutil, multiprocessing
from subprocess import Popen, PIPE, STDOUT

# Definitions

INCLUDES = ['btBulletDynamicsCommon.h',
os.path.join('BulletCollision', 'BroadphaseCollision', 'btDispatcher.h'),
os.path.join('BulletCollision', 'CollisionShapes',     'btHeightfieldTerrainShape.h'),
os.path.join('BulletCollision', 'CollisionShapes',     'btConvexPolyhedron.h'),
os.path.join('BulletCollision', 'CollisionShapes',     'btShapeHull.h'),
os.path.join('BulletCollision', 'CollisionDispatch',   'btCollisionConfiguration.h'),
os.path.join('BulletCollision', 'CollisionDispatch',   'btGhostObject.h'),

os.path.join('BulletDynamics', 'Character',    'btKinematicCharacterController.h'),
os.path.join('BulletDynamics', 'Featherstone', 'btMultiBody.h'),
os.path.join('BulletDynamics', 'Featherstone', 'btMultiBodyConstraintSolver.h'),
os.path.join('BulletDynamics', 'Featherstone', 'btMultiBodyDynamicsWorld.h'),
os.path.join('BulletDynamics', 'Featherstone', 'btMultiBodyLink.h'),
os.path.join('BulletDynamics', 'Featherstone', 'btMultiBodyLinkCollider.h'),

os.path.join('BulletSoftBody', 'btSoftBody.h'),
os.path.join('BulletSoftBody', 'btSoftRigidDynamicsWorld.h'),
os.path.join('BulletSoftBody', 'btDefaultSoftBodySolver.h'),
os.path.join('BulletSoftBody', 'btSoftBodyRigidBodyCollisionConfiguration.h'),
os.path.join('BulletSoftBody', 'btSoftBodyHelpers.h'),

os.path.join('..', 'ammo-a', 'idl_templates.h')]

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

  # Main

  try:
    args = ['-I../bullet3/src', '-c']
    for include in INCLUDES:
      args += ['-include', include]
    emscripten.emcc('glue.cpp', args, 'glue.o')
    assert(os.path.exists('glue.o'))
  finally:
    print ( 'ok' );

if __name__ == '__main__':
  build()

