"""ADT Inventaris Produk + tiga implementasi struktur data.

ADT (Abstract Data Type) mendefinisikan KONTRAK operasi:
    insert(produk)   -> bool      (False bila id_produk sudah ada)
    search(id)       -> Produk | None
    delete(id)       -> bool      (False bila id tidak ditemukan)
    semua()          -> list[Produk]

Implementasi:
    HashInventaris        : Hash Table (Python dict)       <- DIPILIH
    ListInventaris        : Array-based list (Python list)  <- pembanding
    LinkedListInventaris  : Singly Linked List              <- pembanding
"""
from abc import ABC, abstractmethod
from bisect import bisect_left
from typing import Iterable, Optional

from produk import Produk


class InventarisADT(ABC):
    @abstractmethod
    def insert(self, produk: Produk) -> bool: ...

    @abstractmethod
    def search(self, id_produk: str) -> Optional[Produk]: ...

    @abstractmethod
    def delete(self, id_produk: str) -> bool: ...

    @abstractmethod
    def semua(self) -> list: ...

    @abstractmethod
    def bulk_load(self, items: Iterable[Produk]) -> None:
        """Isi awal TANPA cek duplikat (khusus benchmark/seed data)."""

    def semua_terurut(self) -> list:
        """Semua produk terurut menurut ID (default: urutkan hasil semua())."""
        return sorted(self.semua(), key=lambda p: p.id_produk)

    def __len__(self) -> int:
        return len(self.semua())


# ----------------------------------------------------------------------
# 1) Hash Table  (Python dict)  -> insert/search/delete rata-rata O(1)
# ----------------------------------------------------------------------
class HashInventaris(InventarisADT):
    def __init__(self):
        self._data: dict[str, Produk] = {}

    def insert(self, produk: Produk) -> bool:
        if produk.id_produk in self._data:          # O(1)
            return False
        self._data[produk.id_produk] = produk       # O(1)
        return True

    def search(self, id_produk: str) -> Optional[Produk]:
        return self._data.get(id_produk)            # O(1)

    def delete(self, id_produk: str) -> bool:
        return self._data.pop(id_produk, None) is not None   # O(1)

    def semua(self) -> list:
        return list(self._data.values())

    def bulk_load(self, items):
        self._data = {p.id_produk: p for p in items}

    def __len__(self):
        return len(self._data)


# ----------------------------------------------------------------------
# 2) Array-based list (Python list) -> semua operasi by-ID O(n)
# ----------------------------------------------------------------------
class ListInventaris(InventarisADT):
    def __init__(self):
        self._data: list[Produk] = []

    def _index(self, id_produk: str) -> int:
        for i, p in enumerate(self._data):          # O(n)
            if p.id_produk == id_produk:
                return i
        return -1

    def insert(self, produk: Produk) -> bool:
        if self._index(produk.id_produk) != -1:     # cek duplikat O(n)
            return False
        self._data.append(produk)                   # append O(1) amortized
        return True

    def search(self, id_produk: str) -> Optional[Produk]:
        i = self._index(id_produk)                  # O(n)
        return self._data[i] if i != -1 else None

    def delete(self, id_produk: str) -> bool:
        i = self._index(id_produk)                  # O(n)
        if i == -1:
            return False
        self._data.pop(i)                           # geser elemen O(n)
        return True

    def semua(self) -> list:
        return list(self._data)

    def bulk_load(self, items):
        self._data = list(items)

    def __len__(self):
        return len(self._data)


# ----------------------------------------------------------------------
# 3) Singly Linked List (custom ADT) -> pencarian/hapus by-ID O(n)
# ----------------------------------------------------------------------
class _Node:
    __slots__ = ("produk", "next")

    def __init__(self, produk: Produk, next_=None):
        self.produk = produk
        self.next = next_


class LinkedListInventaris(InventarisADT):
    def __init__(self):
        self._head: Optional[_Node] = None
        self._size = 0

    def insert(self, produk: Produk) -> bool:
        if self.search(produk.id_produk) is not None:   # cek duplikat O(n)
            return False
        self._head = _Node(produk, self._head)          # sisip di head O(1)
        self._size += 1
        return True

    def search(self, id_produk: str) -> Optional[Produk]:
        cur = self._head
        while cur is not None:                          # O(n)
            if cur.produk.id_produk == id_produk:
                return cur.produk
            cur = cur.next
        return None

    def delete(self, id_produk: str) -> bool:
        prev, cur = None, self._head
        while cur is not None:                          # cari O(n)
            if cur.produk.id_produk == id_produk:
                if prev is None:
                    self._head = cur.next
                else:
                    prev.next = cur.next                # lepas node O(1)
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def semua(self) -> list:
        hasil, cur = [], self._head
        while cur is not None:
            hasil.append(cur.produk)
            cur = cur.next
        return hasil

    def bulk_load(self, items):
        self._head, self._size = None, 0
        for p in items:
            self._head = _Node(p, self._head)
            self._size += 1

    def __len__(self):
        return self._size


# ----------------------------------------------------------------------
# 4) Sorted array + Binary Search (bisect) -> search O(log n), insert/delete O(n)
# ----------------------------------------------------------------------
class SortedListInventaris(InventarisADT):
    def __init__(self):
        self._ids: list[str] = []          # selalu terurut
        self._data: list[Produk] = []      # sejajar dengan _ids

    def insert(self, produk: Produk) -> bool:
        i = bisect_left(self._ids, produk.id_produk)        # O(log n)
        if i < len(self._ids) and self._ids[i] == produk.id_produk:
            return False
        self._ids.insert(i, produk.id_produk)               # geser elemen O(n)
        self._data.insert(i, produk)
        return True

    def search(self, id_produk: str) -> Optional[Produk]:
        i = bisect_left(self._ids, id_produk)               # O(log n)
        if i < len(self._ids) and self._ids[i] == id_produk:
            return self._data[i]
        return None

    def delete(self, id_produk: str) -> bool:
        i = bisect_left(self._ids, id_produk)               # O(log n)
        if i < len(self._ids) and self._ids[i] == id_produk:
            self._ids.pop(i)                                # geser elemen O(n)
            self._data.pop(i)
            return True
        return False

    def semua(self) -> list:
        return list(self._data)

    def semua_terurut(self) -> list:
        return list(self._data)                             # sudah terurut O(n)

    def bulk_load(self, items):
        self._data = sorted(items, key=lambda p: p.id_produk)
        self._ids = [p.id_produk for p in self._data]

    def __len__(self):
        return len(self._data)


STRUKTUR = {
    "hash": HashInventaris,
    "list": ListInventaris,
    "linked": LinkedListInventaris,
    "sorted": SortedListInventaris,
}
