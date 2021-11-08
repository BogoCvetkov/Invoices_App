import os, sys
from kivy.resources import resource_add_path
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from model.model import Model
from controller import CustomInvoicesBot, InvoicesBot,get_key
from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker,get_color_from_hex
from modules.dates import transform_date
from security.encryption import decrypt_secret
from kivy.config import Config
from dotenv import load_dotenv,find_dotenv

"""
This is the main module used for managing the Graphical Interface (GUI). It is based on the kivy framework
It connects the User interface of the app with the controller module and it's InvoicesBot class
"""

load_dotenv("security/.env")
DEC_KEY = os.getenv("DEC_KEY")

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('kivy', 'window_icon', '../resources/icons/1260673.png')
Config.write()


invoices_period = ''
parsed_info = ''


class MainMenuScreen(Screen):
    pass


class CustomInvoicesScreen(Screen):
    accounts_list = set()
    added_accounts = ObjectProperty(None)
    custom_bot = None
    logged_in = False

    def add_to_list(self):
        account_id = self.ids.account_id.text
        page = self.ids.account_name.text
        if account_id and page:
            check_id = self._check_id_input(input=account_id)
            if check_id:
                account_id = int(account_id)
                if len(self.accounts_list) > 0:
                    id_list = [account_id[1] for account_id in self.accounts_list]
                    if account_id in id_list:
                        self._log_color("red")
                        self.ids.scroll_two.text = "ID Already Added"
                        return None

                account_and_id = (page, account_id)
                self._add_account_button(page, account_id)
                self.accounts_list.add(account_and_id)
                self._log_color("black")
                self.ids.scroll_two.text = "Added to List"

                print(account_and_id)
                print(self.accounts_list)
        else:
            self._log_color("red")
            self.ids.scroll_two.text = "Must Fill Both Fields"

    def add_from_db(self):
        self.clear_list()
        all_accounts = Model.get_account()
        all_accounts = [account[1:] for account in all_accounts]
        for page in all_accounts:
            self._add_account_button(page_name=page[0],
                                     page_id=page[1])
            self.accounts_list.add(page)
        print(all_accounts)

    def remove_button(self, btn):
        btn_id = int(btn.id)

        for item in self.accounts_list:
            if btn_id in item:
                account = item
        self.accounts_list.discard(account)
        self.added_accounts.remove_widget(btn)
        print(self.accounts_list)

    def clear_list(self):
        self.accounts_list.clear()
        self.added_accounts.clear_widgets()

    def login(self):
        if self.logged_in:
            self._log_color("red")
            self.ids.scroll_two.text = "Already Logged In"
        if invoices_period == "":
            self._log_color("red")
            self.ids.scroll_two.text = "Choose Period First"
        else:
            try:
                vat_info = Model.get_billing_info()
                user = Model.get_user()
                decrypted_key = decrypt_secret(DEC_KEY,Model.get_secret())
                secret_key = get_key(decrypted_key)
                self.custom_bot = CustomInvoicesBot(period=invoices_period,
                                                    vat_info=vat_info)
                self.custom_bot.login(username=user[1],
                                      password=user[2],
                                      secret_key=secret_key)
                self.logged_in = True
                self._log_color("black")
                self.ids.scroll_two.text = "You Can Start Scraping"
                self.ids.period_info.text = parsed_info
            except:
                self._log_color("red")
                self.ids.scroll_two.text = "Failed on Logging in"

    def get_invoices(self):
        if not self.logged_in:
            self._log_color("red")
            self.ids.scroll_two.text = "Login First"
        else:
            if not self.accounts_list:
                self._log_color("red")
                self.ids.scroll_two.text = "Accounts List Empty"
            else:
                try:
                    accounts_scraped = self.custom_bot.get_invoices(ad_accounts=self.accounts_list)
                    self._log_color("black")
                    console_message = ",".join([f"Sheet /{item}/ added" for item in accounts_scraped ]).replace(",","\n")
                    self.ids.scroll_two.text = console_message
                except:
                    self._log_color("red")
                    self.ids.scroll_two.text = "Failed Scraping"

    def test(self):
        print(self.custom_bot)

    def close_browser(self):
        self.logged_in = False
        self._log_color("black")
        self.ids.scroll_two.text = "Excel File Created"
        self.custom_bot.close()

    # Private methods used inside of the other methods
    def _add_account_button(self, page_name, page_id):
        page_button = Factory.ListButton(text=f"{page_name}")
        id_list = [id[1] for id in self.accounts_list]
        if page_id not in id_list:
            page_button.id = page_id
            page_button.bind(on_press=self.remove_button)
            self.added_accounts.add_widget(page_button)

    def _check_id_input(self, input):
        if not input.isnumeric():
            self._log_color("red")
            self.ids.scroll_two.text = "Please Enter Only Numbers in the ID Field"
            return False
        else:
            return True

    # Changing console message color
    def _log_color(self, color):
        if color == "red":
            self.ids.scroll_two.color = (1, 0, 0, 0.7)
        else:
            self.ids.scroll_two.color = (0, 0, 0, 0.7)


class VATScreen(Screen):

    def add_vat(self):
        check = self._check_field()
        if check:
            self.ids.vat_log.text = ""
            vat = self.ids.vat_info.text
            Model.insert_billing_info(info=vat)
            self._log_color("black")
            self.ids.vat_log.text = "VAT Info Added"

    def _check_field(self):
        if self.ids.vat_info.text == "":
            self._log_color("red")
            self.ids.vat_log.text = "Please fill VAT info"
            return False
        else:
            return True

    def _log_color(self, color):
        if color == "red":
            self.ids.vat_log.color = (1, 0, 0, 0.7)
        else:
            self.ids.vat_log.color = (0, 0, 0, 0.8)


class AddAccountScreen(Screen):

    def add_account(self):
        check = self._check_field()
        if check:
            account_id = self.ids.add_account_id.text
            account_name = self.ids.add_account_n.text
            check_id = self._check_id_input(input=account_id)
            if check_id:
                try:
                    account_id = int(account_id)
                    res = Model.insert_account(account_name=account_name,
                                               account_id=account_id)
                    self._log_color("black")
                    self.ids.db_log.text = "Account Added"
                except:
                    self._log_color("red")
                    self.ids.db_log.text = "Account Already Added"

    def find_account(self):
        account_name = self.ids.find_account.text
        res = Model.get_account(account_name=account_name)
        output_text = ""
        for account in res:
            output_text += f"{account}\n"
        self.ids.db_console.text = output_text

    def delete_all(self):
        res = Model.delete_all_accounts()
        self._log_color("black")
        self.ids.db_log.text = res

    def remove_account(self):
        account_id = self.ids.remove_account.text
        check_id = self._check_id_input(input=account_id)
        if check_id:
            account_id = int(account_id)
            res = Model.delete_account(account_id=account_id)
            self._log_color("black")
            self.ids.db_log.text = res

    def _check_field(self):
        if self.ids.add_account_n.text == "" or self.ids.add_account_id.text == "":
            self._log_color("red")
            self.ids.db_log.text = "Please fill Both Fields"
            return False
        else:
            return True

    def _check_id_input(self, input):
        if not input.isnumeric():
            self._log_color("red")
            self.ids.db_log.text = "Please Enter Only Numbers in the ID Field"
            return False
        else:
            return True

    def _log_color(self, color):
        if color == "red":
            self.ids.db_log.color = (1, 0, 0, 0.7)
        else:
            self.ids.db_log.color = (0, 0, 0, 0.7)


class FastFlowScreen(Screen):

    def fast_scrape(self):
        all_accounts = Model.get_account()
        user = Model.get_user()
        decrypted_key = decrypt_secret(DEC_KEY, Model.get_secret())
        secret_key = get_key(decrypted_key)
        vat_info = Model.get_billing_info()
        if invoices_period == "":
            self._log_color("red")
            self.ids.flow_log.text = "Choose Period First"
        else:
            try:
                bot = InvoicesBot(invoices_period)
                accounts_scraped = bot.get_invoices(ad_accounts=all_accounts,
                                                    username=user[1],
                                                    password=user[2],
                                                    secret_key=secret_key,
                                                    vat_info=vat_info)
                console_message = ",".join([f"Sheet /{item}/ added" for item in accounts_scraped]).replace(",", "\n")
                self.ids.scroll_text.text = console_message
                self.ids.sent_label.text = "EXCEL FILE \nCREATED"
                self._log_color("black")
                self.ids.flow_log.text = parsed_info
            except:
                self.ids.sent_label.color = (1, 0, 0, 0.7)
                self.ids.sent_label.text = "SCRAPING FAILED"

    def _log_color(self, color):
        if color == "red":
            self.ids.flow_log.color = (1, 0, 0, 0.7)
        else:
            self.ids.flow_log.color = (0, 0, 0, 0.7)


class ScreenSwitch(ScreenManager):
    pass


class InvoiceApp(MDApp):
    def build(self):
        Window.clearcolor = (247 / 255, 247 / 255, 247 / 255, 1)
        return ScreenSwitch()

    def show_date_picker(self):
        date_dialog = MDDatePicker(mode='range',
                                   primary_color=get_color_from_hex("#FEB70E"))
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self,instance,value,range):
        start_date = transform_date(range[0].day,range[0].month,range[0].year)
        end_day = transform_date(range[-1].day,range[-1].month,range[-1].year)
        global invoices_period
        invoices_period = start_date + "_" + end_day
        global parsed_info
        parsed_info = f"Period: {range[0]} / {range[-1]}"
        print(invoices_period)

    def on_cancel(self,instance,value):
        pass


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    InvoiceApp().run()