import argparse
from komiwojazer import Komiwojazer
from macierze import datasets

parser = argparse.ArgumentParser()
parser.add_argument("--alg", required=True, choices=["nn", "naiwny", "heldkarp", "tsp"])
parser.add_argument("--start", type=int, required=True)
parser.add_argument("--dataset", required=True)
args = parser.parse_args()

# pobranie macierzy
if args.dataset not in datasets:
    print("Błąd: nieznany dataset:", args.dataset)
    exit()

macierz = datasets[args.dataset]

k = Komiwojazer()

if args.alg == "nn":
    trasa, dystans = k.najblizszy_sasiad(macierz, args.start)
elif args.alg == "naiwny":
    trasa, dystans = k.naiwny(macierz, args.start)
elif args.alg == "heldkarp":
    trasa, dystans, opt = k.held_karp(macierz, args.start)
elif args.alg == "tsp":
    trasa, dystans = k.tsp(macierz, args.start)

print("Trasa:", trasa)
print("Dystans:", dystans)