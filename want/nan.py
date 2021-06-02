import os
import csv
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QThreadPool, QThread, pyqtSignal, QSize
from PyQt5.uic import loadUiType
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QStatusBar
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from flask import Flask, request, jsonify, Response, redirect, url_for
import threading
from werkzeug.serving import make_server
from PyQt5.QtCore import QThreadPool, QThread, pyqtSignal
import random
from requests_html import HTML
from itertools import cycle
from scrapy.selector import Selector
from threading import Thread
import requests as r
from bs4 import BeautifulSoup
html_form = f"""
                           <!DOCTYPE html>
                       <html lang="en">
                       <head>
                           <meta charset="UTF-8">
                           <title>RePrice</title>
                       </head>
                       <body>
                       <form action="/" method="get">
                           <input type="text" name="EAN">
                           <input type="text" name="title">
                           <input type="submit">

                       </form>
                       </body>
                       </html>"""
html_form2 = """
                    <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>RePrice</title>
                        <style>
                        table, th, td {
                            border: 1px solid black;
                        }
                        th, td {
                            padding: 10px;
                        }
                    </style>
                </head>
                <body>
                <form action="/" method="get">
                    <input type="text" name="EAN">
                    <input type="text" name="title">
                    <input type="submit">

                </form>
                 <h2>Table with Separated Borders</h2>
                    <table>
                        <tr>
                            <th>Prudct</th>
                            <th>Old Price</th>
                            <th>New Price</th>
                            <th>Image</th>
                            <th>time</th>
                        </tr>
                        <tr>
                            <td>NAME PRODUCT</td>
                            <td>20.00</td>
                            <td>19.99</td>
                            <th>
                                        <img src="https://cdn.worldvectorlogo.com/logos/souq-logo-primary-en.svg" alt="HTML5 Icon" style="width:128px;height:128px;">

                            </th>

                        </tr>
                        <tr>
                            <td>2</td>
                            <td>Noor</td>
                            <td>
                            <img class="sealImage"  scr="https://cf1.s3.souqcdn.com/item/2018/05/22/35/17/07/18/item_XXL_35170718_136827577.jpg" alt="HTML5 Icon" style="width:128px;height:128px;">
                            </td>
                        </tr>


                    </table>
                </body>
                </html>"""
process_data = {
    'signin': {
        'url': 'https://sell.souq.com',
        'elements': {
            'signinButton': '//*[@id="loginForm"]/div/span/span/a',
            'emailField': '//*[@id="email"]',
            'continueButton': '//*[@id="continue"]',
            'passwordField': '//*[@id="ap_password"]'
        }
    },
    'reprice_1': {
        'url': 'https://sell.souq.com/fbs-inventory?tab=all',
        'elements': {
            'searchField': '/html/body/section/div/div/main/div/div[2]/div/section/div[1]/div[1]/div[3]/div[1]/div[1]/div/form/fieldset/div/div[1]/ul/li[2]/input',
            'rows': '//*[@id="table-inventory"]/tbody/tr',
            'priceText': '/html/body/section/div/div/main/div/div[2]/div/section/div[2]/div[4]/div[1]/div/div/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr/td[5]/div/span',
            'priceField': '//*[@id="table-inventory"]/tbody/tr/td[5]/form/sc-dynamic-input/input',
            'state': '/html/body/section/div/div/main/div/div[2]/div/section/div[2]/div[4]/div[1]/div/div/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr/td[4]/span'
        }
    },
    'reprice_2': {
        'url': 'https://sell.souq.com/fbs-inventory',
        'elements': {
            'searchField': '//*[@id="main"]/section/div[1]/div[1]/div[3]/div[1]/div[1]/div/form/fieldset/div/div[1]/ul/li[2]/input',
            'firstRow': '//*[@id="table-inventory"]/tbody/tr/td[2]',
            'rows': '//*[@id="table-inventory"]/tbody/tr',
            'priceField': '//input[@id="editableInput"]',
            'updateButton': '//*[@id="offerListitng"]/div[3]/div/div/input'
        }
    }
}
reprice_price = process_data['reprice_1']['elements']['priceText']
reprice_field = process_data['reprice_1']['elements']['priceField']
stat = process_data['reprice_1']['elements']['state']
eann = process_data['reprice_1']['elements']['searchField']
st = ['inventory.status.AVAILABLE', 'Sold Out']
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0"}
insouq = 'https://cf1.s3.souqcdn.com/public/style/img/fbs-rtl.svg'
