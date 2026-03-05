import logging

# set basic logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
    handlers=[logging.StreamHandler()],
)
# set log level of asyncio
logging.getLogger("asyncio").setLevel(logging.WARNING)
# set log level of bleak
logging.getLogger("bleak").setLevel(logging.WARNING)
# set log level of pillow
logging.getLogger("PIL").setLevel(logging.WARNING)