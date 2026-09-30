import json
import os

class FileIO:
    """
    Kelas FileIO merepresentasikan Proses 11.2.1 File I/O pada DFD Level 1.
    Bertugas membaca dan menulis data ke sistem file (external data).
    """

    @staticmethod
    def read_json(filepath):
        """
        Membaca data dari file JSON.
        Input: filepath (str) - path ke file JSON
        Output: dict/list - data yang dibaca dari file, atau struktur kosong jika gagal
        """
        if not os.path.exists(filepath):
            return {} if 'users' in filepath else []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} if 'users' in filepath else []

    @staticmethod
    def write_json(filepath, data):
        """
        Menulis data ke file JSON.
        Input: 
            filepath (str) - path ke file JSON
            data (dict/list) - data yang akan ditulis
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
