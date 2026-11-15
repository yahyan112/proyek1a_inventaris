"""Kelas data Produk untuk Sistem Manajemen Inventaris Produk."""
from dataclasses import dataclass


@dataclass
class Produk:
    """Representasi satu produk pada inventaris e-commerce."""
    id_produk: str      # kunci unik (mis. "P000123")
    nama: str
    kategori: str
    harga: int          # dalam Rupiah
    stok: int

    def __str__(self) -> str:
        return (f"[{self.id_produk}] {self.nama} | {self.kategori} | "
                f"Rp{self.harga:,} | stok: {self.stok}".replace(",", "."))
