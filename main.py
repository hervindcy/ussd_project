import datetime
import re
from storage import Storage
from ui import UI

def main():
    """
    Fungsi utama program. Merepresentasikan alur bisnis (Transfer Pulsa).
    Menghubungkan interaksi antara User (lewat UI) dan Storage.
    """
    storage = Storage('users.json', 'transactions.json')
    biaya_transfer = 2000
    min_transfer = 5000

    UI.display_ussd("Selamat Datang di Layanan Transfer Pulsa")
    
    # LANGKAH 1: Validasi Nomor Pengirim
    nomor_pengirim = UI.get_input("Masukkan nomor pengirim Anda:")
    if not nomor_pengirim:
        UI.display_ussd("Nomor pengirim harus diisi.")
        UI.display_sms(nomor_pengirim or "Unknown", "Transfer pulsa gagal: nomor pengirim belum tersedia.")
        storage.record_transaction({
            "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pengirim": nomor_pengirim, "tujuan": "", "nominal": 0, "biaya": 0, "total": 0,
            "status": "Gagal", "alasan": "Nomor pengirim kosong"
        })
        return

    pengirim_data = storage.get_user(nomor_pengirim)
    if not pengirim_data:
        UI.display_ussd("Nomor pengirim tidak valid/tidak terdaftar.")
        UI.display_sms(nomor_pengirim, "Transfer pulsa gagal: nomor pengirim tidak terdaftar.")
        return

    # LANGKAH 2: Input & Validasi Nomor Tujuan
    nomor_tujuan = UI.get_input("Masukkan nomor tujuan transfer:")
    if not nomor_tujuan:
        UI.display_ussd("Nomor tujuan harus diisi.")
        UI.display_sms(nomor_pengirim, "Transfer pulsa gagal: nomor tujuan belum diisi.")
        storage.record_transaction({"waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pengirim": nomor_pengirim, "tujuan": nomor_tujuan, "nominal": 0, "biaya": 0, "total": 0, "status": "Gagal", "alasan": "Nomor tujuan kosong"})
        return
        
    pattern = r"^08\d{8,11}$"
    if not re.fullmatch(pattern, nomor_tujuan) or not storage.get_user(nomor_tujuan):
        UI.display_ussd("Nomor tujuan tidak valid.")
        UI.display_sms(nomor_pengirim, "Transfer pulsa gagal: nomor tujuan tidak valid.")
        storage.record_transaction({"waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pengirim": nomor_pengirim, "tujuan": nomor_tujuan, "nominal": 0, "biaya": 0, "total": 0, "status": "Gagal", "alasan": "Nomor tujuan tidak valid"})
        return

    # LANGKAH 3: Input & Validasi Nominal
    nominal_input = UI.get_input("Masukkan nominal transfer (misal: 10000):")
    if not nominal_input:
        UI.display_ussd("Nominal transfer harus diisi.")
        UI.display_sms(nomor_pengirim, "Transfer pulsa gagal: nominal transfer belum diisi.")
        storage.record_transaction({"waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pengirim": nomor_pengirim, "tujuan": nomor_tujuan, "nominal": 0, "biaya": 0, "total": 0, "status": "Gagal", "alasan": "Nominal kosong"})
        return
        
    try:
        nominal = float(nominal_input)
    except ValueError:
        UI.display_ussd("Nominal transfer tidak valid.")
        UI.display_sms(nomor_pengirim, "Transfer pulsa gagal: nominal transfer tidak valid.")
        storage.record_transaction({"waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pengirim": nomor_pengirim, "tujuan": nomor_tujuan, "nominal": 0, "biaya": 0, "total": 0, "status": "Gagal", "alasan": "Nominal tidak valid (bukan angka)"})
        return

    if nominal < min_transfer:
        UI.display_ussd("Nominal transfer tidak valid.")
        UI.display_sms(nomor_pengirim, "Transfer pulsa gagal: nominal transfer tidak valid.")
        storage.record_transaction({"waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pengirim": nomor_pengirim, "tujuan": nomor_tujuan, "nominal": nominal, "biaya": 0, "total": 0, "status": "Gagal", "alasan": "Gagal - Nominal Tidak Valid"})
        return

    # LANGKAH 4: Periksa Saldo Pengirim
    total_pembayaran = nominal + biaya_transfer
    if pengirim_data['saldo'] < total_pembayaran:
        UI.display_ussd("Saldo pulsa tidak mencukupi.")
        UI.display_sms(nomor_pengirim, "Transfer pulsa gagal: saldo pulsa tidak mencukupi.")
        storage.record_transaction({"waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pengirim": nomor_pengirim, "tujuan": nomor_tujuan, "nominal": nominal, "biaya": biaya_transfer, "total": total_pembayaran, "status": "Gagal", "alasan": "Saldo tidak cukup"})
        return

    # LANGKAH 5: Tampilkan Ringkasan
    ringkasan = (
        f"Nomor Tujuan      : {nomor_tujuan}\n"
        f"Nominal Transfer  : {nominal}\n"
        f"Biaya Transfer    : {biaya_transfer}\n"
        f"Total             : {total_pembayaran}\n\n"
        "1. Ya\n2. Tidak"
    )
    UI.display_ussd(ringkasan)

    # LANGKAH 6: Validasi Konfirmasi
    konfirmasi = UI.get_input("Masukkan pilihan konfirmasi:")
    if not konfirmasi:
        UI.display_ussd("Konfirmasi harus diisi.")
        UI.display_sms(nomor_pengirim, "Transfer pulsa gagal: konfirmasi transaksi belum diberikan.")
        storage.record_transaction({"waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pengirim": nomor_pengirim, "tujuan": nomor_tujuan, "nominal": nominal, "biaya": biaya_transfer, "total": total_pembayaran, "status": "Gagal", "alasan": "Konfirmasi kosong"})
        return

    if konfirmasi in ["2", "Tidak", "tidak"]:
        UI.display_ussd("Transaksi dibatalkan.")
        UI.display_sms(nomor_pengirim, "Transfer pulsa dibatalkan oleh pengguna.")
        storage.record_transaction({"waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pengirim": nomor_pengirim, "tujuan": nomor_tujuan, "nominal": nominal, "biaya": biaya_transfer, "total": total_pembayaran, "status": "Dibatalkan", "alasan": "Dibatalkan Pengguna"})
        return
    elif konfirmasi not in ["1", "Ya", "ya"]:
        UI.display_ussd("Pilihan konfirmasi tidak valid.")
        UI.display_sms(nomor_pengirim, "Transfer pulsa gagal: pilihan konfirmasi tidak valid.")
        storage.record_transaction({"waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pengirim": nomor_pengirim, "tujuan": nomor_tujuan, "nominal": nominal, "biaya": biaya_transfer, "total": total_pembayaran, "status": "Gagal", "alasan": "Konfirmasi tidak valid"})
        return

    # LANGKAH 7: Proses Transfer
    saldo_pengirim_baru = pengirim_data['saldo'] - total_pembayaran
    saldo_penerima_baru = storage.get_user(nomor_tujuan)['saldo'] + nominal

    storage.update_user_balance(nomor_pengirim, saldo_pengirim_baru)
    storage.update_user_balance(nomor_tujuan, saldo_penerima_baru)

    # LANGKAH 8: Catat Transaksi
    storage.record_transaction({
        "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pengirim": nomor_pengirim,
        "tujuan": nomor_tujuan,
        "nominal": nominal,
        "biaya": biaya_transfer,
        "total": total_pembayaran,
        "status": "Berhasil",
        "alasan": ""
    })

    # LANGKAH 9 & 10: Output Berhasil
    UI.display_ussd(f"Transfer pulsa berhasil.\nPulsa sebesar {nominal}\ntelah dikirim ke {nomor_tujuan}.")
    UI.display_sms(nomor_pengirim, f"Transfer pulsa berhasil ke {nomor_tujuan} sebesar {nominal}.")


if __name__ == "__main__":
    main()
