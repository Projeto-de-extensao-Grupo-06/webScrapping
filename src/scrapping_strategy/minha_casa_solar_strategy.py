from playwright.async_api import Page
from src.batch.scrapping_batch import batch
from src.entity.material_url import MaterialUrl
import re
from src.logging.colors import colors

@batch.register_strategy("www.minhacasasolar.com.br")
def minha_casa_solar_strategy(material_url: MaterialUrl, page: Page):
    print(f"    {colors.cyan}├─{colors.reset} 🌐 Acessando a página do produto...")
    page.goto(material_url.url)

    print(f"    {colors.cyan}├─{colors.reset} ⏳ Aguardando renderização do DOM...")
    page.wait_for_selector("#priceTotal", state="visible")

    locator = page.locator("#priceTotal").first

    price = locator.get_attribute("data-price").__str__()
    price = float(price)

    print(f"    {colors.cyan}├─{colors.reset} 🧩 Valores extraídos: R$ {price}")

    material_url.price = price

    return material_url
