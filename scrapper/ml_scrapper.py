import logging
import re
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from typing_extensions import TypedDict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

logger = logging.getLogger("ScrapperML")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class Installment(TypedDict):
    divider: int
    price: float

class ProductSchema(TypedDict):
    cod_ml: str
    name: str
    url: str
    image_url: str
    price: float
    installment_options: Installment
    price_with_discount: float
    percentual_discount: int
    freight_free: bool
    freight_full: bool

class ScrapperML():
    
    def __init__(
        self,
        search: str | None = None,
        arguments: List[str] | None = None
    ):
        self.url = "https://www.mercadolivre.com.br"
        self.search = search or "computador gamer i7 16gb ssd 1tb"
        self.map = {
            "input_search": {"path": "//*[@id='cb1-edit']"},
            "list_products": {"path": "/html/body/main/div/div[3]/section/ol"},
            "img_product": {"path": ".//img"},
        }
        self.products = []
        firefox_options = Options()
        if arguments:
            for a in arguments:
                firefox_options.add_argument(a)
        try:
            self.browser = webdriver.Firefox(options=firefox_options)
            logger.info(f"Broser inciado... broser: {self.browser.name} - session: {self.browser.session_id}")
        except Exception as e:
            logger.error(f"Erro ao iniciar o navegador: {e}")

    def get_url(self, url: str):
        self.browser.get(url=url)
        logger.info(f"Acessando a URL: {url}")

    def search_fied(self):
        logger.info(f"Dados da busca: {self.search}")
        field = self.browser.find_element(By.XPATH, self.map["input_search"]["path"])
        field.clear()
        field.send_keys(self.search)
        field.send_keys(Keys.RETURN)

    def _extract_ml_code(self, product_url: str) -> str:
        mlb_match = re.search(r"MLB-?(\d+)", product_url)
        mlb_code = mlb_match.group(1) if mlb_match else None
        return mlb_code
    
    def _extract_installment(self, product_installment: str) -> Installment:
        installment_match = re.search(r"(\d+)x\s+R\$\s*([\d.,]+)", product_installment)
        return Installment(
            divider=int(installment_match.group(1)),
            price=float(installment_match.group(2).replace(",", "."))
        )

    def _open_product_for_get_current_url(self, product: WebElement):
        logger.debug("Abrindo aba do produto para extrair codigo mlb.")
        self.browser.execute_script("window.open(arguments[0]);", product.find_element(By.CLASS_NAME, "poly-component__title").get_attribute("href"))
        self.browser.switch_to.window(self.browser.window_handles[-1])
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-pdp-title"))
        )

        mlb_code = self._extract_ml_code(product_url=self.browser.current_url)

        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

        return mlb_code

    def _get_price(self, product: WebElement):
        _product = product.find_element(By.CLASS_NAME, "poly-component__price")

        previous_price = _product.find_elements(By.CLASS_NAME, "andes-money-amount--previous")

        if previous_price:
            price = previous_price[0].find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
        else:
            price = _product.find_element(By.CLASS_NAME, "andes-money-amount--cents-superscript")\
                            .find_element(By.CLASS_NAME, "andes-money-amount__fraction").text

        return float(price.replace('.', '').replace(',', '.'))

    def list_products(self):
        self.get_url(self.url)
        self.search_fied()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-search-layout"))
        )
        section_products = self.browser.find_element(By.XPATH, self.map["list_products"]["path"])
        list_products = section_products.find_elements(By.TAG_NAME, "li")

        logger.info(f"{len(list_products)} produtos encontrados.")

        for i, x in enumerate(list_products):
            x.location_once_scrolled_into_view 
            product = ProductSchema(
                cod_ml= (
                    self._open_product_for_get_current_url(x)
                    if not self._extract_ml_code(
                        product_url=x.find_element(By.CLASS_NAME, "poly-component__title").get_attribute("href")
                    )
                    else self._extract_ml_code(
                        product_url=x.find_element(By.CLASS_NAME, "poly-component__title").get_attribute("href")
                    )
                ),
                name=x.find_element(By.CLASS_NAME, "poly-component__title").text,
                url=x.find_element(By.CLASS_NAME, "poly-component__title").get_attribute("href"),
                image_url=WebDriverWait(x, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "poly-component__picture"))).get_attribute("src"),
                price=self._get_price(product=x),
                installment_options=self._extract_installment(
                    product_installment=x.find_element(By.CLASS_NAME, "poly-price__installments").text
                ),
                price_with_discount=(
                    float(
                        x.find_element(By.CLASS_NAME, "poly-component__price")
                        .find_element(By.CLASS_NAME, "poly-price__current")
                        .find_element(By.CLASS_NAME, "andes-money-amount--cents-superscript")
                        .find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
                        .replace('.', '').replace(',', '.'))
                    if x.find_elements(By.CLASS_NAME, "andes-money-amount--previous")
                    else 0.0
                ),
                percentual_discount=(
                    int(
                        x.find_element(By.CLASS_NAME, "andes-money-amount__discount").text.split(" ")[0].replace("%", ""))
                    if x.find_elements(By.CLASS_NAME, "andes-money-amount--previous")
                    else 0
                ),
                freight_free=(True if x.find_element(By.CLASS_NAME, "poly-component__shipping") else False),
                freight_full=(True if x.find_elements(By.CLASS_NAME, "poly-component__shipped-from") else False)
            )
            logger.info(f".:Produto:.{i}\n{product}")
            self.products.append(product)

        logger.info(f"{len(self.products)} raspados com sucesso!")
        return self.products
