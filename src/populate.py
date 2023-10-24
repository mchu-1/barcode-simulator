# populate.py

"""Generate clonal populations with DNA recordings."""

from utils import encode
import numpy as np
from math import floor

def choose_barcode(n: int) -> int:
  """
  Choose random barcode from a list of barcodes.
  """
  barcode = np.random.randint(1,n)

  return barcode

def generate_recording(n: int, p: float) -> list[int]:
  """
  Generate recording from a list of barcodes.
  """
  recording = []

  P = np.random.uniform()
  first_barcode = choose_barcode(n)
  middle_barcode = n/2
  if P > p or first_barcode > middle_barcode:
    return recording
  else:
    recording.append(first_barcode)
    P = np.random.uniform()

  while P < p:
    new_barcode = choose_barcode(n)
    if new_barcode > 7 and recording[-1] > 7:
      break
    elif new_barcode < 7 and recording[-1] < 7:
      break
    else:
      recording.append(new_barcode)
      P = np.random.uniform()

  return recording


def transfect(n: int, p: float, r: int, population: list) -> list:
  """
  Transfect a population with barcodes and simulate recordings.
  """
  N = len(population)
  round = r
  while round > 0:
    for i in range(N):
      new_recording = generate_recording(n, p)
      population[i].extend(new_recording)
    round -= 1

  return population


def incubate(population: list, d: int) -> list:
  """
  Incubate a population with homogeneous division.
  """
  new_population = population*2**d
  np.random.shuffle(new_population)

  return new_population


def split(population: list, k: int) -> list:
  """
  Split a homogeneous population.
  """
  clones = []
  N = len(population)

  seed = floor(N/k)
  for i in range(0,N,seed):
    clones.append(population[i:i+seed])

  return clones


def sample(clone: list, loss: float) -> list:
  """
  Sample a clone with a given loss.
  """
  np.random.shuffle(clone)
  n = len(clone)
  N = floor(n*(1-loss))
  sample = clone[:N]

  return sample


def simulate_population(F: list, n: int) -> list:
  """
  Simulate population of clones based on a number of splits.
  """
  for i in range(len(F)):
    F[i] = transfect(n, 0.2, 1, F[i])
    F[i] = incubate(F[i], 2)
    F[i] = sample(F[i], 0.5)

  G = []
  for well in F:
    new_wells = split(well, 2)
    G.extend(new_wells)

  return G