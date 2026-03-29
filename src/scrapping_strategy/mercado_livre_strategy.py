from playwright.async_api import Page
from src.batch.scrapping_batch import batch
from src.entity.material_url import MaterialUrl
import re
from src.logging.colors import colors

@batch.register_strategy("www.mercadolivre.com.br")
def mercado_livre_strategy(material_url: MaterialUrl, page: Page):
    print(f"    {colors.cyan}├─{colors.reset} 🌐 Acessando a página do produto...")
    page.goto(material_url.url)

    print(f"    {colors.cyan}├─{colors.reset} ⏳ Aguardando renderização do DOM...")
    page.wait_for_selector(".andes-money-amount__fraction", state="visible")

    real = page.inner_text(".andes-money-amount__fraction")
    cents_locator = page.locator(".andes-money-amount__cents").first

    if cents_locator.is_visible():
        cents = cents_locator.inner_text()
    else:
        cents = "00"

    price = float(f"{re.sub(r'[^\d]', "", real)}.{cents}")

    print(f"    {colors.cyan}├─{colors.reset} 🧩 Valores extraídos: R$ {price} centavos")

    material_url.price = price

    return material_url
