"""
Module for hosting the visualizer module.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import base64

_HTML =\
"""
<html>
<head>
    <title>Visualizer</title>
</head>
<body>
    Hello World!<h1>Hello!</h1>
</body>
</html>
"""

def create_driver():
    global _HTML

    driver = webdriver.Chrome()
    driver.get("data:text/html;base64," + str(base64.b64encode(bytes(_HTML, "utf-8")), "utf-8"))

    return driver