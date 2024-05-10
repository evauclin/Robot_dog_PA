import logging

log = logging.getLogger("Robot-dog")
log.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter("%(levelname)s - %(message)s")
c_handler.setFormatter(c_format)

# Add handlers to the logger
log.addHandler(c_handler)
