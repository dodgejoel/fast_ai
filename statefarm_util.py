from os import path
import csv
import os
import random
import shutil

rand = random.Random()
rand.seed(57)


def make_driver_folds(proot, num_folds):
  drivers_file = open(path.join(proot, 'driver_imgs_list.csv'))
  rows = list(csv.DictReader(drivers_file))
  drivers = list(set(row['subject'] for row in rows))
  rand.shuffle(drivers)
  skip = len(drivers) / num_folds
  driver_folds = [drivers[i* skip:(i + 1) * skip] for i in range(num_folds)]
  leftovers = drivers[(i + 1) * skip:]
  for fold, one_more in zip(driver_folds, leftovers):
    fold.append(one_more)

  fold_map = dict()
  for i, fold in enumerate(driver_folds):
    for driver in fold:
      fold_map[driver] = i

  for row in rows:
    clss = row['classname']
    driver = row['subject']
    srcdir = path.join(proot, 'train', clss)
    destdir = path.join(proot, 'fold_%d' % fold_map[driver], clss)
    src = path.join(srcdir, row['img'])
    dest = path.join(destdir, row['img'])
    try:
      shutil.move(src, dest)
    except IOError:
      # lazily create dirs
      os.makedirs(destdir)
      shutil.move(src,dest)


def make_test_classy(proot):
  os.makedirs(path.join(proot, 'test', 'unknown'))
  for img in os.listdir(path.join(proot, 'test')):
    if img == 'unknown':
      continue
    shutil.move(path.join(proot, 'test', img), path.join(proot, 'test', 'unknown', img))
