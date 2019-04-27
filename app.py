from flask import Flask, request, send_file
import re
import urllib
import matplotlib.pyplot as plt
import random
from PIL import Image

app = Flask(__name__)


def compose_images(a, losowo):
    images = []
    for i in range(a):
        images.append(Image.open("img"+str(i)+".jpg"))
    if int(losowo) == 1:
        images = random.sample(images, a)
    plt.clf()
    if a == 1:
        plt.subplot(1, 1, 1)
        plt.xticks([]), plt.yticks([])
        plt.imshow(images[0], aspect='auto')

    if a == 2:
        for i in range(2):
            plt.subplot(1, 2, i+1)
            plt.xticks([]), plt.yticks([])
            plt.imshow(images[i], aspect='auto')

    if a == 3:
        for i in range(3):
            plt.subplot(2, 2, i+1)
            plt.xticks([]), plt.yticks([])
            plt.imshow(images[i], aspect='auto')

    if a == 4:
        for i in range(4):
            plt.subplot(2, 2, i+1)
            plt.xticks([]), plt.yticks([])
            plt.imshow(images[i], aspect='auto')

    if a == 5:
        for i in range(5):
            if i < 3:
                plt.subplot(2, 3, i+1)
            if i == 3:
                plt.subplot(2, 2, 3)
            if i == 4:
                plt.subplot(2, 2, 4)
            plt.xticks([]), plt.yticks([])
            plt.imshow(images[i], aspect='auto')

    if a == 6:
        for i in range(6):
            plt.subplot(2, 3, i+1)
            plt.xticks([]), plt.yticks([])
            plt.imshow(images[i], aspect='auto')

    if a == 7:
        for i in range(7):
            plt.subplot(3, 3, i+1)
            plt.xticks([]), plt.yticks([])
            plt.imshow(images[i], aspect='auto')

    if a == 8:
        for i in range(8):
            if i < 6:
                plt.subplot(3, 3, i+1)
            if i == 6:
                plt.subplot(3, 2, 5)
            if i == 7:
                plt.subplot(3, 2, 6)
            plt.xticks([]), plt.yticks([])
            plt.imshow(images[i], aspect='auto')
    plt.subplots_adjust(hspace=0, wspace=0)
    plt.savefig('all.jpg', bbox_inches='tight')


@app.route('/mozaika')
def mozaika():
    # pobieranie wartosci parametrow
    losowo = 0
    if request.args.get('losowo'):
        losowo = request.args.get('losowo')
    rozdzielczosc = ""
    if request.args.get('rozdzielczosc'):
        rozdzielczosc = request.args.get('rozdzielczosc')
    if request.args.get("zdjecia"):
        zdjecia = request.args.get("zdjecia")
    else:
        return "brak adresow URL"
    wzor_url = re.findall("http[^,]+", zdjecia)
    if len(wzor_url) > 8:
        return "nieodpowiednia liczba URL"

    # pobieranie obrazkow
    for i in range(len(wzor_url)):
        nazwa = "img"+str(i)+".jpg"
        try:
            urllib.request.urlretrieve(wzor_url[i], nazwa)
        except Exception as e:
            return "<p>Error: %s</p>" % e
    compose_images(len(wzor_url), losowo)

    # ustawienie rozdzielczosci
    img = Image.open('all.jpg')
    if re.fullmatch(r"\d+x\d+", rozdzielczosc):
        first = re.search(r"\d+x", rozdzielczosc)
        first_number = re.search(r"\d+", first.group())
        second = re.search(r"x\d+", rozdzielczosc)
        second_number = re.search(r"\d+", second.group())
        try:
            img = img.resize((int(first_number.group()), int(second_number.group())))
        except Exception as e:
            return "<p>Error: %s</p>" % e
    else:
        img = img.resize((2048, 2048))
    img.save("all.jpg", "JPEG", optimize=True)
    return send_file("all.jpg")


if __name__ == '__main__':
    app.run()
