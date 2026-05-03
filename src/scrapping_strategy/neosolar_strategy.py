from playwright.async_api import Page
from src.batch.scrapping_batch import batch
from src.entity.material_url import MaterialUrl
import re
from src.logging.colors import colors

@batch.register_strategy("www.neosolar.com.br")
def neo_solar_strategy(material_url: MaterialUrl, page: Page):
    print(f"    {colors.cyan}├─{colors.reset} 🌐 Acessando a página do produto...")
    page.goto(material_url.url)

    print(f"    {colors.cyan}├─{colors.reset} ⏳ Aguardando renderização do DOM...")
    page.wait_for_selector(".price", state="visible")

    brute_price = page.inner_text(".price").__str__()

    price = brute_price.replace("R$", "").replace(".", "").replace(",", ".").strip()

    price = float(price)

    print(f"    {colors.cyan}├─{colors.reset} 🧩 Valores extraídos: R$ {price}")

    material_url.price = price

    return material_url
