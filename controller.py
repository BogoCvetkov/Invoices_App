import pyotp
from modules.webdriver import ScrapeBot
from modules.table_tool import TablesTool
from model.model import Model
from datetime import datetime
from modules.dir_maker import create_dir

'''
This Module is combining all the separate modules functionalities from the modules folder and creating
a single class for controlling all the different operations - Authentication,Scraping,Excel Manipulation, CRUD etc.
'''


# URL to use for accessing different ad accounts
base = "https://business.facebook.com/ads/manager/" \
           "billing_history/summary/?act={}&" \
           "pid=p1&" \
           "business_id=11111111111111111111&" \
           "global_scope_id=1111111111111111&" \
           "page=billing_history&tab=summary&" \
           "date={}"


today = datetime.now().strftime("%d_%m")
driver_dir = "Drivers/chromedriver.exe"
invoice_folder = create_dir()



def get_key(key):
    totp = pyotp.TOTP(key)
    return totp.now()


class InvoicesBot:
    ''''
    This is the main Bot class. It's has the purpose of doing all the logging in, scraping and file creation
    in one go. Automating the whole process, to save time for the user. It opens the browser session, does all the work
    and then closes the session. It doesn't allow for browser manipulation from the user in real time.
    '''

    entry_url ="https://business.facebook.com/adsmanager/manage/campaigns?" \
               "act=115891111111111113&" \
               "business_id=115891111111111111515&" \
               "global_scope_id=111111111111115340801515"

    def __init__(self,period):
        self.base_url = base.format("{}",period)

    # Doing all the authentication, scraping and file creation in a single flow/run/method
    def get_invoices(self, ad_accounts, username, password, secret_key, vat_info):
        items_scraped = []
        driver = ScrapeBot(driver_dir)
        driver.login_to_fb(url=self.entry_url,
                           username=username,
                           password=password,
                           two_factor_key=secret_key)
        excel_file = TablesTool(f"{invoice_folder}/invoices_{today}.xlsx",vat_info=vat_info)
        url_list = [(account[-2],self.base_url.format(account[-1])) for account in ad_accounts]
        for account in url_list:
            try:
                driver.get_url(account[1])
                data = driver.scrape_invoices_info()
                excel_file.new_sheet(data=data,
                                     name=account[0])
                items_scraped.append(account[0])
            except:
                pass
        excel_file.close_file()
        driver.close()
        return items_scraped

    @classmethod
    def insert_user(cls, username, password):
        Model.insert_user(username=username,
                          password=password)

    @classmethod
    def insert_account(cls, account_name, account_id):
        try:
            Model.insert_account(account_name=account_name,
                                 account_id=account_id)
        except:
            return "Account Already Added"

    @classmethod
    def get_user(cls):
        return Model.get_user()

    @classmethod
    def get_account(cls, account_name=None, account_id=None):
        return Model.get_account(account_name=account_name,
                                 account_id=account_id)

    @classmethod
    def delete_account(cls,account_id):
        Model.delete_account()


class CustomInvoicesBot(InvoicesBot):

    ''''
    As the name suggests, this is the custom version that Inherits from the upper class. The main idea is that
    here logging in, web scraping and file creation are divided into separate methods, which allows the user to
    control the bot manually and do custom scraping outside the flow.

    So upon instantiating the Object, the browser session is started and lives as long as the user doesn't
    close it. While the session exists, the user is flexible and can scrape as many accounts as he wants, because
    he can manually control the Bot in real time trough the GUI and watch it as it scrapes the data. After that the Bot
    is ready to take the next command from the user and keep on going infinitely. This is not possible in the upper class
    where the flow is predefined and the list of accounts to scrape should be given in advance.
    '''

    def __init__(self,period,vat_info):
        super().__init__(period)
        self.driver = ScrapeBot(driver_dir)
        self.excel_file = TablesTool(table_file=f"{invoice_folder}/invoices_custom_{today}.xlsx",
                                     vat_info=vat_info)

    def login(self,username,password,secret_key):
        self.driver.login_to_fb(url=self.entry_url,
                                username=username,
                                password=password,
                                two_factor_key=secret_key)

    # We're overriding the parent class method, because here it should behave differently
    def get_invoices(self, ad_accounts):
        url_list = [(account[-2], self.base_url.format(account[-1])) for account in ad_accounts]
        items_scraped = []
        for account in url_list:
            try:
                self.driver.get_url(account[1])
                data = self.driver.scrape_invoices_info()
                self.excel_file.new_sheet(data=data,
                                          name=account[0])
                items_scraped.append(account[0])
            except:
                pass
        return items_scraped

    # After finishing with scraping, the user closes the session and saves the file
    # with all the sheets in it from the scraped data in Facebook.#
    def close(self):
        self.excel_file.close_file()
        self.driver.close()


