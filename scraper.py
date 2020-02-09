from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import time
import csv


def get_link(html):
    return html.get_attribute('href')


def get_source(html):
    return html.find_element_by_tag_name('img').get_attribute('src')


def normalize_name(link, src):
    number_with_ext = src.replace(
        'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/', '')
    number = number_with_ext.replace('.png', '')
    return number + '-' + link.replace('https://www.pokemon.com/us/pokedex/', '')


browser = webdriver.Chrome()
browser.get('https://www.pokemon.com/us/pokedex/')

time.sleep(5)
browser.find_element_by_id('cookie-dismisser').click()
browser.find_element_by_id('loadMore').click()

for i in range(0, 100):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

pokemon_links = browser.find_elements_by_xpath('//figure/a')

with open('pokemon.csv', 'w', newline='') as csvfile:
    pokemon_writer = csv.writer(
        csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    pokemon_writer.writerow(['Name', 'Link', 'Image source'])

    for pokemon in range(len(pokemon_links)):

        pokemon_src = get_source(pokemon_links[pokemon])
        pokemon_name = normalize_name(
            pokemon_links[pokemon].get_attribute('href'), pokemon_src)
        pokemon_link = get_link(pokemon_links[pokemon])

        pokemon_writer.writerow([pokemon_name, pokemon_link, pokemon_src])

        print('Name: {}'.format(str(pokemon_name)))
        print('Link: {}'.format(str(pokemon_link)))
        print('Image source: {}\n'.format(str(pokemon_src)))
        urllib.request.urlretrieve(
            pokemon_src, './images/' + pokemon_name + '.png')

browser.quit()


# TO DO
# 1. Add progress bar
# 2. Remove files if they exist
# 3. object oriented
