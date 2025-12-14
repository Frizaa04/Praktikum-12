from abc import ABC , abstractmethod
from dataclasses import dataclass
import logging

logging.basicConfig(
    level= logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

LOGGER = logging.getLogger('checkout')

@dataclass
class Order:
    customer_name : str
    total_price: float
    status: str = "open"\
    
# kode sebelum refactoring
class OrderManager: # melanggar SRP, OCP, dan DIP
    def process_checkout(self, order: Order, payment_method: str):
        print(f"Memulai checkout untuk {order.customer_name}. . .")
        
        # Logika permbayaran yang melanggar OCP/DIP
        if payment_method == "credit_card":
            print("Processing credit card...")

        elif payment_method == "bank_transfer":
            print("Processing transfer bank...")
            
        else:
            print("Metode tidak valid")
            return False
        
        # logika Modifikasi (pelanggaran SRP)
        print(f"mengirim notifiksi ke {order.customer_name}...")
        order.status = "paid"
        return True
    
# Abstraksi (kontak untuk OCP/DIP)
class IPaymentProcessor(ABC):
    """kontrak: semua prosesor pembayaran harus punya method 'proses'"""
    @abstractmethod
    def process(self, order: Order,) -> bool:
        pass

class INotificationService(ABC):
    """Kontrrak: semua layanan notifikasi harus puya method 'send'"""
    @abstractmethod
    def send(self,order:Order):
        pass

# IMPLEMENTASI KONKIRT (PLUG-IN)    
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order)-> bool:
        print("payment: Memproses kartu kredit.")
        return True
    
class EmailNotifier(INotificationService):
    def send(self, order: Order):
        print(f"Notif: Mengirim Email konfirmasi ke {order.customer_name}.")


# Kelas koordinator(SRP & DIP)
class checkoutservice:
    """
    Kelas high Level untuk mengkoordinasi proses transaksi pembayaran.

    Kelas ini memisahkan logika pembayaran dan notifikasi(memenuhi SRP).
    """
    def __init__(self,payment_processor: IPaymentProcessor, notifier: INotificationService):
        """
        Menginisialisasi Checkoutservice dengan dependensi yang diperlukan
        
        Args:
            Payment_processor (UpaymentProcessor): implementasi interdace pembayaran
            notifier(Inotificationservice): implementasi interface notifikasi.
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order)->bool:
        LOGGER.info(f"Memulai checkout untuk {order.customer_name}. Total: {order.total_price}")
        """
        Menjalankan proses checkout dan memvalidasi pembayaran.

        Args:
            order (Order): objek pesanan yang akan diproses.

        Returns:
            bool: True jika checkout sukses, False jika gagal.
        """

        payment_success = self.payment_processor.process(order)

        if payment_success:
            order.status = "paid"
            self.notifier.send(order)
            LOGGER.info("Checkout Sukses. Status pesanan PAID")
            return True
        else:
            LOGGER.info("Pembayaran gagal. transaksi dibatalkan")
            return False
    
# Program Utama

andi_order = Order("Andi", 500000)
email_service = EmailNotifier()

# 1. Inject implementasi Credit Card
cc_processor = CreditCardProcessor()
checkout_cc = checkoutservice(payment_processor= cc_processor, notifier= email_service)
print("--- Skenario 1: Credit card ---")
checkout_cc.run_checkout(andi_order)

# 2 Pembuktian OCP: Menambah Metode Pembayaran QRIS (Tanpa Mengubah Checkoutservice )
class QrisProcessor(IPaymentProcessor):
    def process(self, order: Order)-> bool:
        print("Payment : Memproses Qris.")
        return True

budi_order = Order("Budi", 100000)
qris_processor = QrisProcessor()

# Inject im0lementasi QRIS yang baru dibuat
checkout_qris = checkoutservice(payment_processor=qris_processor, notifier=email_service)
print("\n--- Skenario 2: Pembuktian OCP (QRIS) ---")
checkout_qris.run_checkout(budi_order)