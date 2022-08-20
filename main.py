from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
from webdriver_manager.chrome import ChromeDriverManager
from os import mkdir as makedir
from os.path import isdir, dirname

def get_html(url):
    try:
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get(url)
        html = browser.page_source
        return html
    except Exception as ex:
        print('error: ' + str(ex))
    finally:
        browser.close()
        browser.quit()

def get_dir(path, req):
    for symbol in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
        dir = req.replace(symbol, '')
    return f'{path}\\{dir}'

def save_images(dir, html, max):
    soup = bs(html, 'html.parser')
    idx = 0
    img_urls = [url.find('img').get('src') for url in soup.find_all('div', class_='Pj7 sLG XiG ho- m1e')]
    for url in img_urls:
        urlretrieve(url, f'{dir}/img{str(idx)}.png')
        idx+=1
        if idx==max:
            break

def main():
    request = input('Images request: ')
    path = input('Path to dict with images (empty if code dir): ')
    if path == ''.join(' ' for _ in range(len(path))):
        path=dirname(__file__)
    if not isdir(path):
        print("There's no dict on this path")
        return
    try:
        max_imgs = int(input("What's max count of images?(-1 if everything found): "))
    except:
        print('you must write a number')
    _dir = get_dir(path, request)
    while isdir(_dir):
        if isdir(_dir):
            _dir+='_'
    makedir(_dir)
    url = "https://www.pinterest.com/search/pins/?q="+request
    html = get_html(url)
    save_images(_dir, html, max_imgs)

if __name__ == '__main__':
    main()
