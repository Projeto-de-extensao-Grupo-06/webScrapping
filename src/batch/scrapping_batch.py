import importlib
import pkgutil
from typing import List, Callable, Self
from urllib.parse import urlparse
from src.entity.material_url import MaterialUrl
from src.repository.material_url_repository import update_many_material_url
from src.service.material_url_service import get_all_material_url_cursor
import src.scrapping_strategy as strategies_package
from playwright.sync_api import sync_playwright, Page, ViewportSize
from playwright_stealth.stealth import Stealth
from src.logging.colors import colors

class ScrappingBatch:
    def __init__(self):
        self.chunk: List[MaterialUrl] = []
        self.processed_chunk: List[MaterialUrl] = []
        self.next_cursor: int | None = 0
        self.batch_size: int = 20
        self.strategy = dict[str, Callable[[MaterialUrl, Page], MaterialUrl]]()
        self.strategy_loaded = False
        self.scrapping_instance = sync_playwright().start()

    def _load_strategies(self):
        if self.strategy_loaded:
            return

        print(f"\n{colors.cyan}{colors.bold}⚙️  [SYSTEM INIT] Scanning for scraping strategies in '{strategies_package.__name__}'...{colors.reset}\n")

        loaded_count = 0

        for _, module_name, _ in pkgutil.iter_modules(strategies_package.__path__):
            full_module_name = f"src.scrapping_strategy.{module_name}"

            importlib.import_module(full_module_name)

            print(f"{colors.green}   [+] PLUGGED IN {colors.reset}| {colors.magenta}{module_name:^20}{colors.reset}")
            loaded_count += 1

        print(f"{colors.cyan}   └── {colors.bold}Total strategies active: {loaded_count}{colors.reset}\n")

        self.strategy_loaded = True


    def _get_next_batch(self):
        data = get_all_material_url_cursor(size=self.batch_size, cursor=self.next_cursor)
        self.chunk += data.items
        self.next_cursor = data.next_cursor 

    def register_strategy(self, domain: str):
        def decorator(func: Callable[[MaterialUrl, Page], MaterialUrl]):
            self.strategy[domain] = func
            return func

        return decorator

    def process(self, page: Page = None):
        self._load_strategies()

        if self.next_cursor is not None:
            if page is None:
                print(f"{colors.cyan}🌐 [BROWSER] Launching Chromium instance...{colors.reset}")
                browser = self.scrapping_instance.chromium.launch(headless=False)
                print(f"   └── {colors.green}IDLE{colors.reset} | Browser engine started successfully.")
                ctx = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    viewport=ViewportSize(width=1920, height=1080),
                    device_scale_factor=1,
                )
                Stealth().apply_stealth_sync(ctx)
                page = ctx.new_page()


            print(f"\n{colors.blue}▶ [BATCH START] Fetching next batch (Cursor: {self.next_cursor})...{colors.reset}")
            self._get_next_batch()

            print(f"{colors.cyan}⚙️  Processing {len(self.chunk)} URLs in the current batch...{colors.reset}")

            for chunk in self.chunk:
                url_parsed = urlparse(chunk.url)
                domain = url_parsed.netloc
                strategy = self.strategy.get(domain)

                if strategy is not None:
                    old_price = getattr(chunk, 'price', 'N/A')

                    try:
                        scrapping_result = strategy(chunk, page)
                        new_price = getattr(scrapping_result, 'price', 'N/A')

                        if float(new_price) != float(old_price):
                            self.processed_chunk.append(scrapping_result)
                            print(f"{colors.green}    [✓] PROCESSED{colors.reset} | {colors.magenta}{domain:^20}{colors.reset} | Price: {old_price} -> {colors.green}{new_price}{colors.reset} | {chunk.url}")
                        else:
                            print(f"{colors.cyan}    [=] UNCHANGED{colors.reset} | {colors.magenta}{domain:^20}{colors.reset} | Price remains: {colors.cyan}{old_price}{colors.reset} | {chunk.url}")
                    except Exception as e:
                        print(f"{colors.red}    [✖] FAILED   {colors.reset} | {colors.magenta}{domain:^20}{colors.reset} | {colors.red}Error: {str(e)}{colors.reset} | {chunk.url}")
                else:
                    print(f"{colors.yellow}    [⏭] SKIPPED  {colors.reset} | {colors.magenta}{domain:^20}{colors.reset} | No strategy found | {chunk.url}")

            if self.processed_chunk:
                print(f"{colors.blue}💾 [DATABASE] Saving {len(self.processed_chunk)} updated records...{colors.reset}")
                update_many_material_url(self.processed_chunk)
            else:
                print(f"{colors.yellow}⚠️ [WARNING] No records were updated in this batch.{colors.reset}")

            self.chunk = []
            self.processed_chunk = []

            self.process(page)
        else:
            print(f"\n{colors.green}🏁 [FINISHED] All batches have been processed. No more data to fetch.{colors.reset}")
            print(f"\n{colors.cyan}🔌 [BROWSER] Shutting down Chromium instance...{colors.reset}")
            self.scrapping_instance.stop()
            print(f"   └── {colors.red}OFFLINE{colors.reset} | Browser engine stopped successfully.\n")


batch = ScrappingBatch()