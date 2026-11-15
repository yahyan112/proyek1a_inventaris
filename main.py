"""CLI Sistem Manajemen Inventaris Produk.

Pemakaian:
    python main.py                 # memakai Hash Table (dict) - struktur terpilih
    python main.py --struktur list # (opsional) coba struktur lain
"""
import argparse

from inventaris import STRUKTUR
from produk import Produk

CONTOH = [
    Produk("P001", "Laptop Lenovo ThinkPad T14", "Elektronik", 15_500_000, 12),
    Produk("P002", "Mouse Wireless Logitech M331", "Aksesoris", 250_000, 80),
    Produk("P003", "Kaos Polos Cotton Combed", "Fashion", 65_000, 200),
    Produk("P004", "Kopi Arabika Gayo 250g", "Makanan", 85_000, 45),
]


def input_int(label: str) -> int:
    while True:
        try:
            return int(input(label))
        except ValueError:
            print("  ! Masukkan angka bulat.")


def menu() -> None:
    print("\n=== INVENTARIS PRODUK ===")
    print("1. Daftarkan produk baru   (insert)")
    print("2. Cari produk berdasarkan ID (search)")
    print("3. Hapus produk            (delete)")
    print("4. Tampilkan semua produk")
    print("5. Muat data contoh")
    print("0. Keluar")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--struktur", choices=STRUKTUR, default="hash")
    args = ap.parse_args()
    inv = STRUKTUR[args.struktur]()
    print(f"Struktur data aktif: {type(inv).__name__}")

    while True:
        menu()
        pilih = input("Pilih menu: ").strip()
        if pilih == "1":
            p = Produk(input("ID Produk : ").strip(), input("Nama      : ").strip(),
                       input("Kategori  : ").strip(), input_int("Harga (Rp): "),
                       input_int("Stok      : "))
            print("  ✔ Produk terdaftar." if inv.insert(p)
                  else f"  ✘ ID {p.id_produk} sudah ada.")
        elif pilih == "2":
            p = inv.search(input("ID Produk: ").strip())
            print(f"  ✔ {p}" if p else "  ✘ Produk tidak ditemukan.")
        elif pilih == "3":
            id_ = input("ID Produk yang dihapus: ").strip()
            print("  ✔ Produk dihapus." if inv.delete(id_)
                  else "  ✘ Produk tidak ditemukan.")
        elif pilih == "4":
            data = inv.semua()
            print(f"  Total {len(inv)} produk")
            for p in data:
                print("  -", p)
        elif pilih == "5":
            n = sum(inv.insert(p) for p in CONTOH)
            print(f"  ✔ {n} produk contoh dimuat.")
        elif pilih == "0":
            print("Sampai jumpa!")
            break
        else:
            print("  ! Menu tidak valid.")


if __name__ == "__main__":
    main()
