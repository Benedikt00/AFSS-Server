import logging as log

log.basicConfig(
    format="%(levelname)s: %(message)s", encoding="utf-8", level=log.DEBUG
)  # filename='logs/app.log'

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def logcb(var):
    log.info(f"{type(var)}: {bcolors.OKBLUE} {var} {bcolors.ENDC}")

def logcc(var):
    log.info(f"{type(var)}: {bcolors.OKCYAN} {var} {bcolors.ENDC}")

def logcr(var):
    log.info(f"{type(var)}: {bcolors.WARNING} {var} {bcolors.ENDC}")