from src.batch.scrapping_batch import batch
from src.logging.colors import colors

if __name__ == "__main__":
    solarway_logo = f"""{colors.cyan}{colors.bold}
  ____   ___  _        _    ____  __        ___  __   __
 / ___| / _ \\| |      / \\  |  _ \\ \\ \\      / / \\ \\ \\ / /
 \\___ \\| | | | |     / _ \\ | |_) | \\ \\ /\\ / / _ \\ \\ V / 
  ___) | |_| | |___ / ___ \\|  _ <   \\ V  V / ___ \\ | |  
 |____/ \\___/|_____/_/   \\_\\_| \\_\\   \\_/\\_/_/   \\_\\|_|  

         W E B   S C R A P I N G   B A T C H
{colors.reset}"""
    print(solarway_logo)
    print(f"{colors.yellow}🚀 [SYSTEM ALERT] Initiating web scraping batch process. Please wait...{colors.reset}\n")
    batch.process()
    print(f"\n{colors.green}✅ [SUCCESS] Batch processing finished successfully!{colors.reset}")