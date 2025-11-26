from flask import Flask, render_template
import os
import random

def create_app():
    # set this equal to the location where you installed the app!
    # it needs to fetch the static wallpapers + templates from here...
    install_location = "/home/tim/waifu-dot-local/waifudotlocal/"

    # Set app name to the name of this script/package
    app = Flask(__name__,
                template_folder=install_location + 'templates/',
                static_folder=install_location + 'static/')

    imgExtensions = ["png", "jpeg", "jpg"]
    allImages = list()

    imageFolder = install_location + 'static/waifus/'

    def chooseRandomImage(directory):
        try:
            for img in os.listdir(directory):
                ext = img.split(".")[len(img.split(".")) - 1]
                if (ext in imgExtensions):
                    allImages.append(img)
            choice = random.randint(0, len(allImages) - 1)
            chosenImage = allImages[choice]
        except FileNotFoundError as e:
            return ("An error occurred:", str(e))
        else:
            return chosenImage

    @app.route("/hello-world")
    def hello_world():
        return "<p>Hello, World! App root path: " + app.root_path + "</p>"

    @app.route("/")
    def home_page(errorMessage="", waifuImage="", hidden="hidden"):
        randomImage = chooseRandomImage(imageFolder)
        if "An error occurred:" in randomImage:
            errorMessage = randomImage
            hidden = "" # Un-hide error message
        else:
            waifuImage = "/static/waifus/" + randomImage
        return render_template('main.html',
                                errorMessage=errorMessage,
                                waifuImage=waifuImage,
                                hidden=hidden)
    
    return app
