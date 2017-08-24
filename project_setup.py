import os
import random
import shutil

from os import path
from Queue import Queue

random.seed(57)  # my favorite prime

def make_validation_set(proot, proportion=.1):
  """
  given a project root with a train dir containing class subdirectories
  move the given proportion of them to a valid set reproducing the class directories.
  """
  assert 'valid' not in os.listdir(proot)
  assert 'train' in os.listdir(proot)
  for class_ in os.listdir(path.join(proot, 'train')):
    os.makedirs(path.join(proot, 'valid', class_))
    imgs = os.listdir(path.join(proot, 'train', class_))
    take = int(proportion * len(imgs))
    random.shuffle(imgs)
    for img in imgs[:take]:
      src = path.join(proot, 'train', class_, img)
      dest = path.join(proot, 'valid', class_, img)
      print('moving from %s to %s' % (src, dest))
      shutil.move(src, dest)

def make_sample(proot, num):
  """
  given a project root with train, valid and test directories
  make a sample copy of this tree as a subdirectory of proot.
  each class will contain at most num examples in both train and valid.
  the test set will contain at most num examples.
  """
  setd = set(os.listdir(proot))
  assert 'sample' not in setd
  to_cp = ['train', 'valid']
  for d in to_cp:
    assert d in setd
  assert 'test' in setd
      
  for d in to_cp:
    for class_ in os.listdir(path.join(proot, d)):
      os.makedirs(path.join(proot, 'sample', d, class_))
      chosen = random.sample(os.listdir(path.join(proot, d, class_)), num)
      for f in chosen:
        src = path.join(proot, d, class_, f)
        dest = path.join(proot, 'sample', d, class_, f)
        print('copying %s to %s' % (src, dest))
        shutil.copy(src, dest)
              
  os.makedirs(path.join(proot, 'sample', 'test'))
  for f in random.sample(os.listdir(path.join(proot, 'test')), num):
    src = path.join(proot, 'test', f)
    dest = path.join(proot, 'sample', 'test', f)
    print('copying %s to %s' %(src, dest))
    shutil.copy(src, dest)
