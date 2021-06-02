from nan import *
class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server(f'127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()
    def run(self):
        print('Server Is Runing ...')
        self.srv.serve_forever()
    def shutdown(self):
        print('Server Is Closed ...')
        self.srv.shutdown()
class rel(QThread):
    email = pyqtSignal(str)
    password = pyqtSignal(str)
    patdd = pyqtSignal(str)
    nump = pyqtSignal(str)
    ean = pyqtSignal(str)
    price = pyqtSignal(str)
    path = pyqtSignal(str)
    def __init__(self, pathh, em, pwd):
        QThread.__init__(self)
        self.email = em
        self.password = pwd
        self.path = pathh
    def run(self):
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': '129.146.180.91:3128',
            'ftpProxy': '129.146.180.91:3128',
            'sslProxy': '129.146.180.91:3128',
            'noProxy': '129.146.180.91:3128'  # set this value as desired
        })

        options = Options()
        options.add_argument('--headless')

        driver = webdriver.Firefox(executable_path=self.path, timeout=15, proxy=proxy)
        elements = process_data['signin']['elements']
        reprice_url = process_data['reprice_1']['url']
        driver.get(process_data['signin']['url'])
        self.nump.emit('Open FireFox')
        self.nump.emit('Open Souq')
        try:
            driver.find_element_by_xpath(elements['signinButton']).click()
        except:
            time.sleep(2)
            driver.find_element_by_xpath(elements['signinButton']).click()
        try:
            driver.find_element_by_xpath(elements['emailField']).send_keys(f'{self.email}' + Keys.ENTER)
            self.nump.emit('Set Email')
        except:
            self.nump.emit('Set Email 2')
            time.sleep(2)
            driver.find_element_by_xpath(elements['emailField']).send_keys(f'{self.email}' + Keys.ENTER)
        for i in range(50):
            self.nump.emit('.')
            self.nump.emit('..')
            self.nump.emit('...')
        try:
            time.sleep(3)
            driver.find_element_by_xpath(elements['continueButton']).click()
        except:
            time.sleep(3)
            driver.find_element_by_xpath(elements['continueButton']).click()
        try:
            driver.find_element_by_xpath(elements['passwordField']).send_keys(f'{self.password}' + Keys.ENTER)
        except:
            time.sleep(3)
            driver.find_element_by_xpath(elements['passwordField']).send_keys(f'{self.password}' + Keys.ENTER)
        self.nump.emit('Set Password')
        driver.get(reprice_url)
        inn = 40
        onn = 1
        while onn < inn:
            self.nump.emit(f" For Approve : ({onn})")
            time.sleep(1)
            onn += 1
        try:
            time.sleep(4)
            self.patdd.emit(' ☺ ')
            driver.get(reprice_url)
            time.sleep(5)
            e = driver.find_element_by_xpath(eann)
            e.send_keys(Keys.ENTER)
            self.nump.emit(f'Welcome')
        except:
            self.nump.emit(f'Need  Approved !!')
        global server
        app = Flask(__name__)
        server = ServerThread(app)
        server.start()
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'GET':
                if 'EAN' in request.args:
                    name = request.args['EAN']
                    price = request.args['title']
                    e = driver.find_element_by_xpath(eann)
                    time.sleep(2)
                    e.send_keys(f'{name}')
                    time.sleep(1.5)
                    e.send_keys(Keys.ENTER)
                    time.sleep(2)
                    state = driver.find_element_by_xpath(stat)
                    print(state.text)
                    if state.text in st:
                        remove(ean=name)
                    e.clear()
                    try:
                        first_option = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, reprice_price)))
                        first_option.click()
                        e_field = driver.find_element_by_xpath(reprice_field)
                        e_field.clear()
                        e_field.send_keys(f'{price}', Keys.ENTER)
                        print(name)
                    except:
                        time.sleep(1.5)
                        first_option = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, reprice_price)))
                        first_option.click()
                        e_field = driver.find_element_by_xpath(reprice_field)
                        e_field.clear()
                        e_field.send_keys(f'{price}', Keys.ENTER)
                    return html_form

        @app.route('/run')
        def run():
            return html_form2
class checker(QThread):
    pat = pyqtSignal(str)
    s = r.Session()
    EAN = pyqtSignal(str)
    on_fire = pyqtSignal(str)
    def __init__(self):
        QThread.__init__(self)
    def run(self):
        while True:
            with open('set.csv', newline='') as f:
                Ean = csv.DictReader(f)
                for ena in Ean:
                    try:
                        self.on_fire.emit(f'{ena["ean"]}')
                        baseUrl = f'https://egypt.souq.com/eg-ar/{ena["ean"]}/s/?as=1'
                        content = self.s.get(url=baseUrl,
                                             headers=headers,
                                             proxies={'http': '168.119.137.56:3128'},
                                             timeout=9).content
                        content = Selector(text=content)
                        seller = content.css('span.unit-seller-link').css('b::text').get()
                        priceText = content.css('h3.price').get()
                        html = HTML(html=priceText)
                        if seller == 'Top.System':
                            up = UPThread(ean=ena['ean'])
                            up.start()
                            continue
                        elif seller != 'Top.System':
                            mm = html.find('h3', first=True).text
                            gpg = '\xa0جنيه'
                            m = mm.strip(gpg)
                            m1 = m[:len(gpg)]
                            price = float(m1)
                            if price < float(ena['limit']):
                                print('ohh noooo')
                                print(seller, ':', price, f' - {ena}\n', '__________')
                            elif price >= float(ena['limit']):
                                self.EAN.emit(f'{ena["ean"]}, {price}')
                                os.environ['NO_PROXY'] = '127.0.0.1'
                                r.get(f'http://127.0.0.1:5000/?EAN={ena["ean"]}&title={price - 0.02}')
                                print(seller, ':', price, f' - {ena}\n', '__________')
                    except:
                        continue
def remove(ean):
    updatedlist = []
    with open("set.csv", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != ean:
                updatedlist.append(row)
        updatefile(updatedlist)
def updatefile(updatedlist):
    with open("set.csv", "w", newline="") as f:
        Writer = csv.writer(f)
        Writer.writerows(updatedlist)
        print("File has been updated")
class UPThread(threading.Thread):
    def __init__(self, ean):
        threading.Thread.__init__(self)
        self.ean = ean
    def run(self):
        link = self.filter_link(ean=self.ean)
        s_p = []
        pr = []
        if link == None:
            print('-' * 30, 'No Seller', '-' * 30)
            exit()
        else:
            get = r.get(link)
            scr = get.content
            soup = BeautifulSoup(scr, 'lxml')
            all_price = soup.find_all("div", {"class": "field price-field"})
            all_seller = soup.find_all("div", {"class": "field seller-name"})
            souq = soup.find_all("div", {"class": "field clearfix labels"})
            for i in range(len(all_seller)):
                p = all_price[i].text
                nn = p.split('EGP')
                s = all_seller[i].text
                price, seller = nn[0].strip(), s.strip()
                if ',' in price:
                    price = price.split(',')
                    pha = float(price[0] + price[1])
                    price = float(round(pha, 2))
                sahra = souq[i].text
                IS_SOUQ = sahra.strip()
                if IS_SOUQ == '':
                    IS_SOUQ = False
                else:
                    IS_SOUQ = True
                all_dict = {f"seller": f"{seller}", f"price": f"{price}", f"souq": f"{IS_SOUQ}"}
                s_p.append(all_dict)
            ng = len(s_p) / 2
            if ng == 1:
                print('Seller is You')
                pass
            for all_pric in range(int(ng)):
                pr.append(s_p[all_pric])
            self.filter_seller(lst=pr, ea=self.ean)
            return pr
    def filter_link(self, ean):
        n = r.get(f'https://egypt.souq.com/eg-en/{ean}/s/?as=1')
        scr = n.content
        soup = BeautifulSoup(scr, 'lxml')
        link_sellers = soup.find_all("a", {"class": "show-for-medium bold-text"})
        for i in range(len(link_sellers)):
            link = link_sellers[i]['href']
            return link
    def filter_seller(self, lst, ea):
        try:
            ls = []
            ls2 = []
            alli = lst
            num = 0
            for i in alli:
                if i['seller'] != 'Top.System':
                    num += 1
                    continue
                num += 1
                ls.append(i)
                ls2.append(num)
            nh = ls2[0]
            ls.append(alli[nh])
            self.filter_reprice(lst=ls, ea=ea)
            return ls
        except:
            pass
    def filter_reprice(self, lst, ea):
        lss = []
        num = lst
        for i in num:
            lss.append(i)
        print(
            f"""SELLER : {lss[0]['seller']} | {lss[1]['seller']}\nPRICE  :    {lss[0]['price']}     {lss[1]['price']}\nSOUQ   :    {lss[0]['souq']}      {lss[1]['souq']}\n""",
            '-' * 30)
        price_me = float(lss[0]['price'])
        price_seller = float(lss[1]['price'])
        new = price_seller - price_me
        stat_souq = lss[1]['souq']
        if stat_souq == 'True':
            if new > 1:
                try:
                    r.get(f'http://127.0.0.1:5000/?EAN={ea}&title={price_seller - 0.02}')
                    print('Need CHANGE !', ea)
                except:
                    pass
        elif stat_souq == 'False':
            if new > 1:
                try:
                    print('Need CHANGE With High Price', ea)
                    r.get(f'http://127.0.0.1:5000/?EAN={ea}&title={price_seller - 0.02}')
                except:
                    pass
def exit():
    quit()
