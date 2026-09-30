from file_io import FileIO

class Storage:
    """
    Kelas Storage merepresentasikan D1 Storage pada DFD Level 1.
    Bertindak sebagai perantara data di memori yang mengambil dari dan menyimpan ke File I/O.
    """
    def __init__(self, users_file="users.json", tx_file="transactions.json"):
        self.users_file = users_file
        self.tx_file = tx_file
        self.users_data = {}
        self.tx_data = []
        self.load_data()

    def load_data(self):
        """
        Memuat data dari File I/O ke dalam Storage.
        """
        self.users_data = FileIO.read_json(self.users_file)
        self.tx_data = FileIO.read_json(self.tx_file)

    def get_user(self, phone):
        """
        Mendapatkan data pengguna berdasarkan nomor HP.
        Input: phone (str) - nomor handphone
        Output: dict - data pengguna jika ada, None jika tidak
        """
        return self.users_data.get(phone)

    def update_user_balance(self, phone, new_balance):
        """
        Memperbarui saldo pengguna dan menyimpannya ke File.
        Input: phone (str), new_balance (float)
        """
        if phone in self.users_data:
            self.users_data[phone]['saldo'] = new_balance
            FileIO.write_json(self.users_file, self.users_data)

    def record_transaction(self, tx_record):
        """
        Mencatat riwayat transaksi dan menyimpannya ke File.
        Input: tx_record (dict) - data record transaksi
        """
        self.tx_data.append(tx_record)
        FileIO.write_json(self.tx_file, self.tx_data)
