from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

# [Pastikan import logging ada di awal file]

# Konfigurasi dasar: Semua log level INFO ke atas akan ditampilkan
# Format: Waktu - Level Nama Kelas/Fungsi - Pesan
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
# Tambahkan logger untuk kelas yang akan kita gunakan
LOGGER = logging.getLogger(' << Proses Orderan >> ')
LOGGER2 = logging.getLogger(' >> Menu << ')
LOGGER3 = logging.getLogger(' -- Promosi -- ')
LOGGER4 = logging.getLogger(' ++ Payment ++ ')
LOGGER5 = logging.getLogger(' == Cetak Struk == ')

# -- DATA CLASS: Item --
@dataclass
class Item:
    """
    Kelas untuk menyimpan data string(name) dan integer(price)
    """
    name: str
    price: int
    

# ++ SRP: Katalog Harga ++
class PriceCatalog(ABC):
    """
    Interface/antarmuka/kontrak untuk seluruh katalog harga
    Kontrak: Semua menu yang tersedia mempunyai method 'get_item'(gunanya untuk mendapatkan item)
    dan 'calculate'(gunanya untuk menghitung total harga).

    Kelas ini mendefinisikan method abstrak 'get_item' dan 'calculate' yang harus
    diimplementasikan pada setiap kelas turunan dengan menambahkan kelas menu baru.
    
    Aturan:
    - Tidak boleh diinstansi langsung pada kelas abstrak.
    - Harus diimplementasikan oleh setiap katalog harga baru.
    """
    @abstractmethod
    def get_item(self, name: str) -> Item:
        """
        Mendapatkan item berdasarkan nama item/menu dari katalog harga

        Args:
            name (str): Nama item/menu pada menu yang ingin diambil dari katalog harga
        
        Returns:
            Item: Objek item yang berisi nama dan harga dalam menu
        
        Raises:
            ValueError: Jika nama item/menu tidak ditemukan di dalam katalog harga,
            akan menghentikan proses orderannya
        """
        pass

    @abstractmethod
    def calculate(self, items: list[str]) -> int:
        """
        Menghitung total harga setiap yang dipesan pada item/menu

        Args:
            items (list[str]): Daftar nama item/menu yang dipilih kepada pelanggan

        Returns:
            int: Total harga seluruh item berdasarkan pelanggan yang dipesan pada katalog harga
        """
        pass

class CafePriceCatalog(PriceCatalog):
    """
    Implementasi detail konkret dari kelas PriceCatalog untuk katalog harga menu kafe.
    
    Kelas ini mengimplementasikan daftar item/menu dan harga dalam bentuk data dictionary(pustakawan),
    ini dapat digunakan pada menampilkan menu kafe(plug-in) di kelas high-level(OrderProcessor)
    tanpa mengubah/modifikasi pada kelas high-level(OrderProcessor) (memenuhi DIP/OCP).
    Kelas ini menyediakan operasi, yaitu:
    - Mengambil item berdasarkan nama menu yang tersedia
    - Menghitung total harga yang dipesan pelanggan

    Raises:
        ValueError: Jika nama item/menu tidak ditemukan di dalam katalog harga,
                    akan menghentikan proses orderannya
    """
    PRICES = {
        "espresso": 20000,
        "latte": 30000,
        "cappuccino": 28000,
        "americano": 22000,
        "macchiato": 32000,
        "dalgona coffe": 23000
    }

    def get_item(self, name: str) -> Item:
        """
        Mengambil satu item/menu yang diminta pada pelanggan

        Args:
            name (str): Nama item/menu yang diminta pelanggan

        Raises:
            ValueError: Jika nama item/menu tidak ditemukan di dalam katalog harga,
            akan menghentikan proses orderannya

        Returns:
            Item: Objek item yang berisi nama dan harga dalam menu
        """
        if name not in self.PRICES:
            LOGGER2.error(f"Item dengan nama '{name}' tidak ada di menu")
            raise ValueError("Pesanan dihentikan, silahkan sesuaikan menu cafe ini")
        else:
            price = self.PRICES[name]
            item = Item(name=name, price=price)
            return item

    def calculate(self, items: list[str]) -> int:
        """
        Menghitung total harga setiap yang dipesan pada item/menu

        Args:
            items (list[str]): Daftar nama item/menu yang dipilih kepada pelanggan

        Returns:
            int: Total harga seluruh item berdasarkan pelanggan yang dipesan pada katalog harga
        """
        total = 0
        for name in items:
            item = self.get_item(name)
            total += item.price
        LOGGER2.info(f"Total harga untuk {items}: {total}")
        return total


# || OCP + DIP: Strategi Promosi ||
class PromotionStrategy(ABC):
    """
    Interface/antarmuka/kontrak untuk seluruh promosi tersedia
    Kontrak: Semua promosi yang tersedia mempunyai
    method 'apply'(gunanya untuk mendapatkan promonya, yang tergantung dapat berapa potongan harga).

    Kelas ini mendefinisikan method abstrak 'apply' yang harus diimplementasikan
    pada setiap kelas turunan dengan menambahkan kelas promosi baru.
    
    Aturan:
    - Tidak boleh diinstansi langsung pada kelas abstrak
    - Harus diimplementasikan pada setiap strategi promosi baru
    """
    @abstractmethod
    def apply(self, total: int) -> int:
        """
        Menyesuaikan total harga item/menu yang dipesan pelanggan
        berdasarkan strategi promosi.

        Args:
            total (int): Total harga awal sebelum mendapatkan potongan harga pada promosi.

        Returns:
            int: Total harga setelah mendapatkan potongan harga pada promosi.
        """
        pass

class DineInPromo(PromotionStrategy):
    """
    Implementasi detail konkret dari kelas PromotionStrategy untuk strategi promosi Dine-In.
    
    Kelas ini mendefinisikan aturan potongan harga khusus pada metode Dine-In
    yang tergantung seberapa banyak harga yang dipesan pada pelanggan,
    ini dapat digunakan pada menerapkan promosi Dine-in(plug-in) di kelas high-level(OrderProcessor)
    tanpa mengubah/modifikasi pada kelas high-level(OrderProcessor) (memenuhi DIP/OCP).
    """
    def apply(self, total: int) -> int:
        """
        Menyesuaikan total harga item/menu yang dipesan pelanggan
        berdasarkan strategi promosi.

        Args:
            total (int): Total harga awal sebelum mendapatkan potongan harga pada promosi.

        Returns:
            int: Total harga setelah mendapatkan potongan harga pada promosi.
        """
        discount = 0
        if total > 100000:
            discount = 10000
            LOGGER3.info(f"Promo Dine-In mendapatkan potongan harga {discount}")
        else:
            LOGGER3.info("Promo Dine-In tidak mendapatkan potongan harga")
        
        final_total = total - discount
        LOGGER3.info(f"Total sesudah mendapatkan promo Dine-In: {final_total}")
        return final_total

class TakeAwayPromo(PromotionStrategy):
    """
    Implementasi detail konkret dari kelas PromotionStrategy untuk strategi promosi Take Away.
    
    Kelas ini mendefinisikan aturan potongan harga khusus pada metode Take Away
    yang tergantung seberapa banyak harga yang dipesan pada pelanggan,
    ini dapat digunakan pada menerapkan promosi Take Away(plug-in) di kelas high-level(OrderProcessor)
    tanpa mengubah/modifikasi pada kelas high-level(OrderProcessor) (memenuhi DIP/OCP).
    """
    def apply(self, total: int) -> int:
        """
        Menyesuaikan total harga item/menu yang dipesan pelanggan
        berdasarkan strategi promosi.

        Args:
            total (int): Total harga awal sebelum mendapatkan potongan harga pada promosi.

        Returns:
            int: Total harga setelah mendapatkan potongan harga pada promosi.
        """
        discount = 0
        if total > 80000:
            discount = 5000
            LOGGER3.info(f"Promo Take Away mendapatkan potongan harga {discount}")
        else:
            LOGGER3.info("Promo Take Away tidak mendapatkan potongan harga")
        
        final_total = total - discount
        LOGGER3.info(f"Total sesudah mendapatkan promo Take Away: {final_total}")
        return final_total

class HappyHourPromo(PromotionStrategy):
    """
    Implementasi detail konkret dari kelas PromotionStrategy untuk strategi promosi Happy Hour.
    
    Kelas ini mendefinisikan aturan potongan harga khusus pada metode Happy Hour,
    ini dapat digunakan pada menerapkan promosi Happy Hour(plug-in) di kelas high-level(OrderProcessor)
    tanpa mengubah/modifikasi pada kelas high-level(OrderProcessor) (memenuhi DIP/OCP).
    """
    def apply(self, total: int) -> int:
        """
        Menyesuaikan total harga item/menu yang dipesan pelanggan
        berdasarkan strategi promosi.

        Args:
            total (int): Total harga awal sebelum mendapatkan potongan harga pada promosi.

        Returns:
            int: Total harga setelah mendapatkan potongan harga pada promosi.
        """
        discount_rate = 0.2
        discount_amount = int(total * discount_rate)
        final_total = total - discount_amount
        
        LOGGER3.info(f"Promo Happy Hour mendapatkan potongan harga {discount_amount}")
        LOGGER3.info(f"Total sesudah mendapatkan promo Happy Hour: {final_total}")
        return final_total


# << OCP + DIP: Strategi Payment >>
class PaymentStrategy(ABC):
    """
    Interface/antarmuka/kontrak untuk seluruh metode pembayaran tersedia
    Kontrak: Semua metode pembayaran yang tersedia mempunyai
    method 'apply_fee'(gunanya untuk menyetujui dengan memakai metode pembayaran dengan adanya biaya tambahan).

    Kelas ini mendefinisikan method abstrak 'apply_fee' yang harus diimplementasikan
    pada setiap kelas turunan dengan menambahkan kelas metode pembayaran baru.
    
    Aturan:
    - Tidak boleh diinstansi langsung pada kelas abstrak
    - Harus diimplementasikan pada setiap strategi metode pembayaran baru
    """
    @abstractmethod
    def apply_fee(self, total: int) -> int:
        """
        Menyesuaikan total harga item/menu yang dipesan pelanggan
        berdasarkan strategi metode pembayaran.

        Args:
            total (int): Total harga yang sebelum dikenai biaya tambahan
            pada pemilihan metode pembayaran

        Returns:
            int: Total harga setelah dipilih metode pembayaran dengan biaya tambahan.
        """
        pass

class CashPayment(PaymentStrategy):
    """
    Implementasi detail konkret dari kelas PaymentStrategy untuk strategi metode pembayaran tunai(uang fisik).
    
    Kelas ini mendefinisikan pada metode pembayaran tunai tanpa dikenai tambahan biaya,
    ini dapat digunakan pada menerapkan metode pembayaran tunai(plug-in) di kelas high-level(OrderProcessor)
    tanpa mengubah/modifikasi pada kelas high-level(OrderProcessor) (memenuhi DIP/OCP).
    """
    def apply_fee(self, total: int) -> int:
        """
        Menyesuaikan total harga item/menu yang dipesan pelanggan
        berdasarkan strategi metode pembayaran.

        Args:
            total (int): Total harga yang sebelum dikenai biaya tambahan
            pada pemilihan metode pembayaran

        Returns:
            int: Total harga setelah dipilih metode pembayaran dengan biaya tambahan.
        """
        LOGGER4.info(f"Total semua tanpa dikenai biaya tambahan: {total}")
        return total

class QrisPayment(PaymentStrategy):
    """
    Implementasi detail konkret dari kelas PaymentStrategy untuk strategi metode pembayaran Qris.
    
    Kelas ini mendefinisikan pada metode pembayaran Qris dengan adanya tambahan biaya,
    ini dapat digunakan pada menerapkan metode pembayaran Qris(plug-in) di kelas high-level(OrderProcessor)
    tanpa mengubah/modifikasi pada kelas high-level(OrderProcessor) (memenuhi DIP/OCP).
    """
    def apply_fee(self, total: int) -> int:
        """
        Menyesuaikan total harga item/menu yang dipesan pelanggan
        berdasarkan strategi metode pembayaran.

        Args:
            total (int): Total harga yang sebelum dikenai biaya tambahan
            pada pemilihan metode pembayaran

        Returns:
            int: Total harga setelah dipilih metode pembayaran dengan biaya tambahan.
        """
        biaya = 1000
        LOGGER4.info(f"Metode pembayaran Qris dikenai biaya {biaya}")
        final_total = total + biaya
        LOGGER4.info(f"Total semua dengan biaya metode pembayaran Qris: {final_total}")
        return final_total


class EWalletPayment(PaymentStrategy):
    """
    Implementasi detail konkret dari kelas PaymentStrategy untuk strategi metode pembayaran E-Wallet.
    
    Kelas ini mendefinisikan pada metode pembayaran E-Wallet dengan adanya tambahan biaya,
    ini dapat digunakan pada menerapkan metode pembayaran E-Wallet(plug-in) di kelas high-level(OrderProcessor)
    tanpa mengubah/modifikasi pada kelas high-level(OrderProcessor) (memenuhi DIP/OCP).
    """
    def apply_fee(self, total: int) -> int:
        """
        Menyesuaikan total harga item/menu yang dipesan pelanggan
        berdasarkan strategi metode pembayaran.

        Args:
            total (int): Total harga yang sebelum dikenai biaya tambahan
            pada pemilihan metode pembayaran

        Returns:
            int: Total harga setelah dipilih metode pembayaran dengan biaya tambahan.
        """
        biaya = 1500
        LOGGER4.info(f"Metode pembayaran E-Wallet dikenai biaya {biaya}")
        final_total = total + biaya
        LOGGER4.info(f"Total semua dengan biaya metode pembayaran E-Wallet: {final_total}")
        return final_total


# ++ SRP: Receipt Printer ++
class ReceiptPrinter:
    """
    Kelas Utilitas(maksudnya, kelas yang dibuat untuk menyediakan fungsi atau layanan pendukung(support))
    yang bertanggung jawab untuk mencetak struk pada pembelian pelanggan.
    
    Kelas ini mempunyai satu tanggun jawab, yaitu
    memperlihatkan informasi transaksi(daftar item/menu dan total harga) pada pemesanan
    dalam bentuk struk (memenuhi SRP)
    """
    def print_receipt(self, items, total):
        """
        Mencetak struk pembelian berdasarkan item/menu yang dipesan dan total harga akhir transaksi.

        Args:
            items (list[str]): Daftar nama item/menu yang dipilih kepada pelanggan
            total (int): Total harga akhir yang harus dibayarkan pada pelanggan
                         setelah promosi dan tambahan biaya pemilihan metode pembayaran.
        """
        LOGGER5.info("Mencetak struk pembelian:")
        for item in items:
            LOGGER5.info(f" {item} -")
        LOGGER5.info(f"Total: {total}")


# >> DIP + OCP + SRP: Order Processor <<
class OrderProcessor:
    """
    Kelas High-Level yang bertanggung jawab mengkoordinasi seluruh proses transaksi pemesanan pelanggan.
    
    Kelas OrderProcessor tidak secara langsunng mengimplementasikan detail konkrit
    pada detail perhitungan harga, promosi, metode pembayaran, maupun cetak struk.
    Semua perilaku, didelegasikan ke objek lain melalui abstraksi (antarmuka/interface).
    
    Kelas ini sudah memenuhi pada prinsip:
    - SRP sebagai koordinator alur transaksi.
    - DIP yang bergantungan pada abstraksi, bukan melalui implementasi detail konkret.
    - OCP yang dapat diperluas dengan strategi pembayaran baru, katalog harga ataupun strategi promosi baru
      tanpa mengubah/modifikasi kode dalam kelas ini.
    """
    def __init__(self,
                 promo: PromotionStrategy,
                 payment: PaymentStrategy,
                 catalog: PriceCatalog,
                 printer: ReceiptPrinter):
        """
        Menginisialisasi pada kelas OrderProcessor dengan strategi dan bahan bahan yang dibutuhkan.
        
        Seluruh depedensi akan disuntikan melalui konstruktor(depedency injection) agar kelas
        OrderProcessor tidak langsung implementasi detail konkret.

        Args:
            promo (PromotionStrategy): 
            Strategi promosi yang akan diterapkan pada total harga transaksi dengan potongan harga.
            
            payment (PaymentStrategy):
            Strategi metode pembayaran yang dipilih metode pembayaran pada pelanggan dengan
            biaya tambahan transaksi.
            
            catalog (PriceCatalog):
            Katalog harga yang digunakan untuk mengambil/menampilkan harga item
            dan menghitung total harga pesanan.
            
            printer (ReceiptPrinter): Bahan yang bertanggung jawab untuk mencetak struk transaksi.
        """
        self.promo = promo
        self.payment = payment
        self.catalog = catalog
        self.printer = printer

    def process(self, items):
        """
        Menjalankan seluruh proses alur transaksi pemesanan tanpa mengganggu logika lainnya.

        Proses yang dilakukan:
        1. Menghitung total harga pada item dari katalog harga yang dipesan pada pelanggan.
        2. Menerapkan strategi promosi yang dipilih.
        3. Menambahkan biaya berdasarkan metode pembayaran yang dipilih pada pelanggan.
        4. Mencetak struk transaksi
        Args:
            items (list[str]): Daftar nama item/menu yang dipilih kepada pelanggan

        Returns:
            int: Total harga akhir setelah promo dan biaya tambahan yang diterapkan
        """
        total = self.catalog.calculate(items)
        total = self.promo.apply(total)
        total = self.payment.apply_fee(total)
        self.printer.print_receipt(items, total)
        return total


# !! Contoh penggunaan !!

print("=== PESANAN 1 ===")
processor = OrderProcessor(
    promo = DineInPromo(),
    payment = QrisPayment(),
    catalog = CafePriceCatalog(),
    printer = ReceiptPrinter()
)
processor.process(["espresso", "latte", "americano"])

print("\n=== PESANAN 2 (OCP EXTENSION TEST) ===")
processor = OrderProcessor(
    promo = HappyHourPromo(),  # fitur promo baru, tidak mengubah kode lain
    payment = CashPayment(),
    catalog = CafePriceCatalog(),
    printer = ReceiptPrinter()
)
processor.process(["latte", "latte", "latte"])

# ?? Contoh penggunaan yang salah ??

print("\n=== PESANAN YANG SALAH ===")
processor = OrderProcessor(
    promo = TakeAwayPromo(),
    payment = EWalletPayment(),
    catalog = CafePriceCatalog(),
    printer = ReceiptPrinter()
)
processor.process(["americano", "cappuccino", "nasi goreng"]) # <- nasi goreng tidak dalam menu cafe, Memunculkan ValueError dan "pesanan dihentikan"