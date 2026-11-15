# Proyek 1A – Sistem Manajemen Inventaris Produk (Hash Table)

CLI Python dengan ADT `InventarisADT` (insert, search, delete) dan tiga implementasi:
`HashInventaris` (dict, **terpilih**), `ListInventaris`, `LinkedListInventaris`.

```
python main.py                  # CLI (hash table)
python main.py --struktur list  # coba struktur lain: list | linked | hash
python benchmark.py             # ukur insert/search/delete untuk n = 1.000 / 10.000 / 100.000
```
Hasil ringkas (µs/op, n=100.000): search dict 0,56 vs list 1.855 vs linked 1.805 → dict O(1), lainnya O(n).
