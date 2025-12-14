from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    level= logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )

LOGGER = logging.getLogger('Register')
# sebelum melakukan refactoring
# ValidatorManager memiliki lebih dari satu tanggung jawab.
class ValidatorManager:
    def validate(self, student, course):
        # Validasi SKS
        if student.total_sks >= 144:
            return "DITOLAK: SKS melebihi batas"


        # Validasi prasyarat
        if course.prerequisite is not None:
            if course.prerequisite not in student.completed_courses:
                return "DITOLAK: Prasyarat belum terpenuhi"


        # Validasi IPK
        if student.gpa < 2.5:
            return "DITOLAK: IPK tidak mencukupi"


        return "DITERIMA"

# Implementasi DIP dan OCP
class Validator(ABC):
    """
    Interface untuk aturan validasi registrasi mahasiswa.

    Setiap kelas yang mengimplementasikan interface ini
    harus menyediakan mekanisme validasi spesifik
    terhadap data mahasiswa dan mata kuliah.
    """
    @abstractmethod
    def validate(self, student, course):
        """
        Melakukan validasi terhadap mahasiswa dan mata kuliah.

        Args:
            student (Student): Objek mahasiswa yang akan divalidasi.
            course (Course): Objek mata kuliah yang akan diambil.
        Returns:
            bool: 
                - True jika validasi lolos.
                - False jika validasi gagal.
        """
        pass

# Validasi SKS
class SKSvalidator(Validator):
    def validate(self, student, course):
        if student.total_sks >= 144 :
            LOGGER.info("SKS melebihi batas")
            return False
        return True
    
# Validasi persyaratan matkul
class PrerequisiteValidator(Validator):
    def validate(self, student, course):
        if course.prerequisite and course.prerequisite not in student.completed_courses:
            LOGGER.info("Tidak Memenuhi Prasyarat")
            return False
        return True

# Validasi IPK
class IPKValidator(Validator):
    def validate(self,student, course):
        if student.IPK < 2.8:
            LOGGER.info("IPK Tidak Mencukupi")
            return False
        return True
# Sekarang setiap kelas hanya memiliki satu tanggung jawab 
# tanpa memengaruhi class lain sesuai dengan SRP

# Penerapan DIP karena RegistrationValidator bergantung pada abstraksi Validator
# OCP diterapkan karena kita bisa menambah validator baru tanpa mengubah kode RegistrationValidator
class RegistrationValidator:
    """
    Service untuk menjalankan proses validasi registrasi mahasiswa.

    Kelas ini bertanggung jawab untuk mengeksekusi
    sekumpulan aturan validasi yang diimplementasikan
    melalui interface Validator.
    """
    def __init__(self, validators):
        """
        Konstruktor RegistrationValidator.

        Args:
            validators (list[Validator]): 
                Daftar aturan validasi yang akan dijalankan.
        """
        self.validators = validators

    def validate(self, student, course):
        """
        Menjalankan seluruh aturan validasi registrasi.

        Proses validasi akan berhenti jika salah satu
        aturan tidak terpenuhi.

        Args:
            student (Student): Mahasiswa yang melakukan registrasi.
            course (Course): Mata kuliah yang akan diambil.

        Returns:
            bool:
                - True jika semua validasi lolos.
                - False jika salah satu validasi gagal.
        """
        for validator in self.validators:
            if not validator.validate(student, course):
                LOGGER.info("Registrasi Ditolak")
                return False
        LOGGER.info("Registrasi Berhasil")
        return True
        

# Pembuktian OCP(Menambahkan aturan baru tanpa merubah kode lama)
class PaymentValidator(Validator):
    def validate(self,student,course):
        if not student.is_paid:
            LOGGER.info("Pembayaran Belum Lunas")
            return False
        return True

# Membuat Objek
class Student:
    def __init__(self, total_sks, completed_courses, IPK, is_paid):
        self.total_sks = total_sks
        self.completed_courses = completed_courses
        self.IPK = IPK
        self.is_paid = is_paid

class Course:
    def __init__(self, name, prerequisite=None):
        self.name = name
        self.prerequisite = prerequisite

# Program utama
student = Student(
    total_sks=124,
    completed_courses=["Algoritma", "Struktur Data"],
    IPK=2.9,
    is_paid=True
)

course = Course(
    name="Pemrograman Lanjut",
    prerequisite="Struktur Data"
)

validators = [
    SKSvalidator(),
    PrerequisiteValidator(),
    IPKValidator(),
    PaymentValidator()
]

Validator = RegistrationValidator(validators)
result = Validator.validate(student, course)

print(result)