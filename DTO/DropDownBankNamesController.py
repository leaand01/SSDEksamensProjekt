from Services.BankFeeRepository import LocalDB, Banks
from Infrastructure.DbInitializer import dict_banks


local_db = LocalDB(dict_banks)
banks = Banks(local_db)

dropdown_bank_names = list(banks.get_all().keys())
