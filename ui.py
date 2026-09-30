class UI:
    """
    Kelas UI merepresentasikan Proses 11.2.0 User Interface pada DFD Level 1.
    Menangani input dari user dan menampilkan output USSD/SMS.
    """
    
    @staticmethod
    def display_ussd(message):
        """
        Menampilkan pesan bergaya pop-up USSD.
        Input: message (str)
        """
        print("\n=========================================")
        print("              USSD *858#")
        print("=========================================")
        print(message)
        print("=========================================\n")

    @staticmethod
    def display_sms(phone, message):
        """
        Mensimulasikan pengiriman SMS ke nomor tertentu.
        Input: phone (str), message (str)
        """
        print(f"\n[SIMULASI SMS ke {phone}]")
        print("-" * 41)
        print(message)
        print("-" * 41 + "\n")

    @staticmethod
    def get_input(prompt):
        """
        Meminta input dari user.
        Input: prompt (str)
        Output: string input dari user
        """
        return input(f"{prompt}\n> ").strip()
