from views.main import InvoiceApp
import os, sys
from kivy.resources import resource_add_path
from kivy.lang import Builder
from model.model import Model


# This is the entry point for the App


Builder.load_file("views/accounts_menu.kv")
Builder.load_file("views/vat_info.kv")
Builder.load_file("views/add_account.kv")
Builder.load_file("views/fast_flow.kv")

InvoiceApp.kv_file = "views/main_menu.kv"

Model.db = "model/database.db"

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    InvoiceApp().run()