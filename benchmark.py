"""Benchmark insert / search / delete untuk tiga struktur data.

Jalankan:  python benchmark.py
Metode: tiap struktur diisi n produk (bulk_load), lalu masing-masing operasi
dijalankan Q kali pada ID acak (seed tetap); hasil = rata-rata mikrodetik/op.
"""
import json
import random
import time

from inventaris import (HashInventaris, LinkedListInventaris, ListInventaris,
                        SortedListInventaris)
from produk import Produk

UKURAN = [1_000, 10_000, 100_000]
Q = 200
STRUKTUR = [("Hash Table (dict)", HashInventaris),
            ("Array List (list)", ListInventaris),
            ("Linked List", LinkedListInventaris),
            ("Sorted List + bisect", SortedListInventaris)]


def buat(n):
    return [Produk(f"P{i:07d}", f"Produk {i}", "Umum", 10_000 + i % 997, i % 100)
            for i in range(n)]


def waktu(fn, args_list):
    t0 = time.perf_counter()
    for a in args_list:
        fn(a)
    return (time.perf_counter() - t0) / len(args_list) * 1e6   # µs/op


def main():
    hasil = {}
    for n in UKURAN:
        data = buat(n)
        random.Random(1).shuffle(data)   # urutan acak agar sort tidak "kebetulan" cepat
        rnd = random.Random(42)
        ids_ada = rnd.sample([p.id_produk for p in data], Q)
        baru = [Produk(f"N{i:07d}", "Baru", "Umum", 1, 1) for i in range(Q)]
        for nama, kls in STRUKTUR:
            inv = kls()
            inv.bulk_load(data)
            r = {
                "insert": waktu(inv.insert, baru),     # termasuk cek duplikat ID
                "search": waktu(inv.search, ids_ada),
                "delete": waktu(inv.delete, ids_ada),
                "tampil_urut": waktu(lambda _: inv.semua_terurut(), range(5)) / 1000,  # ms/op
            }
            hasil.setdefault(nama, {})[n] = r
            print(f"n={n:>7,} {nama:<18} insert={r['insert']:>10.2f} µs  "
                  f"search={r['search']:>10.2f} µs  delete={r['delete']:>10.2f} µs  tampil_urut={r['tampil_urut']:>9.2f} ms")
        print()
    with open("hasil_benchmark.json", "w") as f:
        json.dump(hasil, f, indent=2)


if __name__ == "__main__":
    main()
