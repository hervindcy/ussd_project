# PSPEC (Process Specification)

## 1. Process Name & ID

**Process ID:** 2.0
**Process Name:** Memproses Transfer Pulsa
**System:** USSD `*858#`

---

## 2. Input Data Items

| No | Input Data       | Keterangan                              |
| -- | ---------------- | --------------------------------------- |
| 1  | Nomor Pengirim   | Nomor pelanggan yang melakukan transfer |
| 2  | Nomor Tujuan     | Nomor pelanggan penerima pulsa          |
| 3  | Nominal Transfer | Jumlah pulsa yang akan ditransfer       |
| 4  | Konfirmasi       | Persetujuan pengguna terhadap transaksi |

---

## 3. Output Data Items

| No | Output Data       | Keterangan                                         |
| -- | ----------------- | -------------------------------------------------- |
| 1  | Pesan Status USSD | Informasi berhasil, gagal, atau dibatalkan         |
| 2  | Notifikasi SMS    | Informasi hasil transaksi yang dikirim melalui SMS |
| 3  | Catatan Transaksi | Data transaksi dan statusnya                       |

---

## 4. Data Store

### D1 – Data Pengguna

Menyimpan:

* Nomor Pengirim
* Nomor Tujuan
* Status pelanggan
* Saldo pulsa

### D2 – Catatan Transaksi

Menyimpan:

* Nomor Pengirim
* Nomor Tujuan
* Nominal transfer
* Biaya transfer
* Waktu transaksi
* Status transaksi
* Alasan kegagalan atau pembatalan

---

# 5. Logic Processing / Algorithm

## 1. VALIDASI NOMOR PENGIRIM

```text
TERIMA Nomor Pengirim dari session USSD.

IF Nomor Pengirim kosong / tidak tersedia THEN
    TAMPILKAN pesan USSD:
        "Nomor pengirim harus diisi."

    KIRIM SMS:
        "Transfer pulsa gagal: nomor pengirim belum tersedia."

    CATAT transaksi:
        Status = "Gagal - Nomor Pengirim Kosong"

    STOP proses.
ELSE
    LANJUTKAN ke proses berikutnya.
END IF
```

---

## 2. INPUT DAN VALIDASI NOMOR TUJUAN

```text
MINTA pengguna memasukkan Nomor Tujuan.

IF Nomor Tujuan kosong THEN
    TAMPILKAN pesan USSD:
        "Nomor tujuan harus diisi."

    KIRIM SMS:
        "Transfer pulsa gagal: nomor tujuan belum diisi."

    CATAT transaksi:
        Status = "Gagal - Nomor Tujuan Kosong"

    STOP proses.

ELSE IF Nomor Tujuan tidak valid / tidak terdaftar THEN
    TAMPILKAN pesan USSD:
        "Nomor tujuan tidak valid."

    KIRIM SMS:
        "Transfer pulsa gagal: nomor tujuan tidak valid."

    CATAT transaksi:
        Status = "Gagal - Nomor Tujuan Tidak Valid"

    STOP proses.

ELSE
    LANJUTKAN ke proses berikutnya.
END IF
```

---

## 3. INPUT DAN VALIDASI NOMINAL

```text
MINTA pengguna memasukkan Nominal Transfer.

IF Nominal Transfer kosong THEN
    TAMPILKAN pesan USSD:
        "Nominal transfer harus diisi."

    KIRIM SMS:
        "Transfer pulsa gagal: nominal transfer belum diisi."

    CATAT transaksi:
        Status = "Gagal - Nominal Kosong"

    STOP proses.

ELSE IF Nominal Transfer tidak memenuhi aturan transfer THEN
    TAMPILKAN pesan USSD:
        "Nominal transfer tidak valid."

    KIRIM SMS:
        "Transfer pulsa gagal: nominal transfer tidak valid."

    CATAT transaksi:
        Status = "Gagal - Nominal Tidak Valid"

    STOP proses.

ELSE
    LANJUTKAN ke proses berikutnya.
END IF
```

---

## 4. VALIDASI SALDO PENGIRIM

```text
AMBIL Saldo Pulsa dari D1.

AMBIL Biaya Transfer.

HITUNG Total Pembayaran:
    Total = Nominal Transfer + Biaya Transfer

IF Saldo Pulsa < Total THEN
    TAMPILKAN pesan USSD:
        "Saldo pulsa tidak mencukupi."

    KIRIM SMS:
        "Transfer pulsa gagal: saldo pulsa tidak mencukupi."

    CATAT transaksi:
        Status = "Gagal - Saldo Tidak Mencukupi"

    STOP proses.
ELSE
    LANJUTKAN ke proses berikutnya.
END IF
```

---

## 5. TAMPILKAN RINGKASAN DAN KONFIRMASI

```text
TAMPILKAN ringkasan transaksi:

    Nomor Tujuan      : [Nomor Tujuan]
    Nominal Transfer  : [Nominal Transfer]
    Biaya Transfer    : [Biaya Transfer]
    Total              : [Total]

TAMPILKAN pilihan:
    1. Ya
    2. Tidak

MINTA pengguna memasukkan Konfirmasi.
```


---

## 6. VALIDASI KONFIRMASI PENGGUNA

```text
TERIMA input Konfirmasi dari pengguna.

IF Konfirmasi kosong THEN
    TAMPILKAN pesan USSD:
        "Konfirmasi harus diisi."

    KIRIM SMS:
        "Transfer pulsa gagal: konfirmasi transaksi belum diberikan."

    CATAT transaksi:
        Status = "Gagal - Konfirmasi Kosong"

    STOP proses.

ELSE IF Konfirmasi = "1" OR Konfirmasi = "Ya" THEN
    LANJUTKAN ke proses transfer pulsa.

ELSE IF Konfirmasi = "2" OR Konfirmasi = "Tidak" THEN
    TAMPILKAN pesan USSD:
        "Transaksi dibatalkan."

    KIRIM SMS:
        "Transfer pulsa dibatalkan oleh pengguna."

    CATAT transaksi:
        Status = "Dibatalkan"

    STOP proses.

ELSE
    TAMPILKAN pesan USSD:
        "Pilihan konfirmasi tidak valid."

    KIRIM SMS:
        "Transfer pulsa gagal: pilihan konfirmasi tidak valid."

    CATAT transaksi:
        Status = "Gagal - Konfirmasi Tidak Valid"

    STOP proses.
END IF
```

---

## 7. PROSES TRANSFER PULSA

```text
AMBIL data:
    Nomor Pengirim
    Nomor Tujuan
    Nominal Transfer
    Total Pembayaran

LAKUKAN pengurangan pulsa pengirim:
    Saldo Pengirim =
        Saldo Pengirim - Total Pembayaran

LAKUKAN penambahan pulsa penerima:
    Saldo Penerima =
        Saldo Penerima + Nominal Transfer

IF pengurangan pulsa pengirim BERHASIL
   AND penambahan pulsa penerima BERHASIL THEN

    SET Status Transfer = "Berhasil"

    LANJUTKAN ke proses pencatatan transaksi.

ELSE

    JIKA transaksi gagal THEN
        JANGAN menetapkan transaksi sebagai berhasil.

        TAMPILKAN pesan USSD:
            "Transfer pulsa gagal diproses."

        KIRIM SMS:
            "Transfer pulsa gagal diproses. Silakan coba kembali."

        CATAT transaksi:
            Status = "Gagal - Proses Transfer"

        STOP proses.
    END IF
END IF
```

---

## 8. CATAT TRANSAKSI

```text
SIMPAN data transaksi ke D2 Catatan Transaksi:

    Nomor Pengirim
    Nomor Tujuan
    Nominal Transfer
    Biaya Transfer
    Total Pembayaran
    Waktu Transaksi
    Status Transaksi

IF Status Transfer = "Berhasil" THEN
    Status Transaksi = "Berhasil"
ELSE
    Status Transaksi = "Gagal"
END IF
```

---

## 9. TAMPILKAN PESAN STATUS

```text
IF Status Transaksi = "Berhasil" THEN

    TAMPILKAN pesan USSD:
        "Transfer pulsa berhasil.
         Pulsa sebesar [Nominal Transfer]
         telah dikirim ke [Nomor Tujuan]."

ELSE IF Status Transaksi = "Dibatalkan" THEN

    TAMPILKAN pesan USSD:
        "Transaksi dibatalkan."

ELSE

    TAMPILKAN pesan USSD:
        "Transfer pulsa gagal diproses."

END IF
```

---

## 10. KIRIM NOTIFIKASI SMS

```text
IF Status Transaksi = "Berhasil" THEN

    KIRIM SMS:
        "Transfer pulsa berhasil ke
         [Nomor Tujuan] sebesar
         [Nominal Transfer]."

ELSE IF Status Transaksi = "Dibatalkan" THEN

    KIRIM SMS:
        "Transfer pulsa dibatalkan oleh pengguna."

ELSE

    JIKA terdapat alasan kegagalan tertentu THEN
        KIRIM SMS sesuai alasan kegagalan.

    ELSE
        KIRIM SMS:
            "Transfer pulsa gagal diproses.
             Silakan coba kembali."
    END IF

END IF

SELESAI.
```

---

# 6. Matriks Kondisi dan Output

| Kondisi | Pesan USSD | SMS | Status |
|---|---|---|---|
| Nomor pengirim kosong | Nomor pengirim harus diisi | Nomor pengirim belum tersedia | Gagal |
| Nomor tujuan kosong | Nomor tujuan harus diisi | Nomor tujuan belum diisi | Gagal |
| Nomor tujuan tidak valid | Nomor tujuan tidak valid | Nomor tujuan tidak valid | Gagal |
| Nominal kosong | Nominal transfer harus diisi | Nominal transfer belum diisi | Gagal |
| Nominal tidak valid | Nominal transfer tidak valid | Nominal transfer tidak valid | Gagal |
| Saldo tidak cukup | Saldo pulsa tidak mencukupi | Saldo pulsa tidak mencukupi | Gagal |
| Konfirmasi kosong | Konfirmasi harus diisi | Konfirmasi belum diberikan | Gagal |
| Konfirmasi tidak valid | Pilihan konfirmasi tidak valid | Pilihan konfirmasi tidak valid | Gagal |
| Pengguna memilih Tidak | Transaksi dibatalkan | Transfer pulsa dibatalkan | Dibatalkan |
| Transfer berhasil | Transfer pulsa berhasil | Transfer pulsa berhasil | Berhasil |
| Transfer gagal diproses | Transfer pulsa gagal diproses | Transfer pulsa gagal diproses | Gagal |

---

# 7. Ringkasan Structured English

```text
BEGIN PROCESS "Memproses Transfer Pulsa"

1. VALIDATE Nomor Pengirim
   IF kosong THEN
       TAMPILKAN USSD
       KIRIM SMS
       CATAT kegagalan
       STOP
   END IF

2. INPUT Nomor Tujuan
   VALIDATE Nomor Tujuan
   IF kosong / tidak valid THEN
       TAMPILKAN USSD
       KIRIM SMS
       CATAT kegagalan
       STOP
   END IF

3. INPUT Nominal Transfer
   VALIDATE Nominal
   IF kosong / tidak valid THEN
       TAMPILKAN USSD
       KIRIM SMS
       CATAT kegagalan
       STOP
   END IF

4. CHECK Saldo Pengirim
   HITUNG Total = Nominal + Biaya

   IF Saldo < Total THEN
       TAMPILKAN USSD
       KIRIM SMS
       CATAT kegagalan
       STOP
   END IF

5. TAMPILKAN Ringkasan Transaksi
   MINTA Konfirmasi

6. VALIDATE Konfirmasi
   IF kosong THEN
       TAMPILKAN USSD
       KIRIM SMS
       CATAT kegagalan
       STOP

   ELSE IF "Tidak" THEN
       TAMPILKAN USSD
       KIRIM SMS
       CATAT pembatalan
       STOP

   ELSE IF bukan "Ya" THEN
       TAMPILKAN USSD
       KIRIM SMS
       CATAT kegagalan
       STOP
   END IF

7. PROCESS Transfer
   KURANGI pulsa pengirim
   TAMBAHKAN pulsa penerima

8. RECORD Transaction
   SIMPAN seluruh data transaksi

9. TAMPILKAN Status melalui USSD

10. KIRIM Notifikasi melalui SMS

END PROCESS
```

# 8. End Result

```text
SUCCESS
    → Pulsa pengirim berkurang
    → Pulsa penerima bertambah
    → Transaksi dicatat sebagai BERHASIL
    → Pesan berhasil ditampilkan melalui USSD
    → SMS berhasil dikirim

FAILURE
    → Transaksi tidak dinyatakan berhasil
    → Alasan kegagalan dicatat
    → Pesan kegagalan ditampilkan melalui USSD
    → SMS kegagalan dikirim

CANCELLED
    → Transaksi dibatalkan
    → Tidak ada transfer pulsa
    → Status dicatat sebagai DIBATALKAN
    → Pesan pembatalan ditampilkan melalui USSD
    → SMS pembatalan dikirim
```