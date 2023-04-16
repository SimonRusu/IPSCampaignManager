import pathlib
import shutil
import os
import zipfile
from flask import send_file
from uuid import uuid4
from werkzeug.utils import secure_filename
from config import imagesDir

def generateZipImages(images):
    ranFolder = str(uuid4())
    zipRef = ranFolder + '.zip'
    imagesFolder = os.path.join(pathlib.Path(__file__).parent.parent.resolve(), imagesDir, ranFolder)
    os.makedirs(imagesFolder)

    for i in images:
        i.save(os.path.join(imagesFolder, secure_filename(str(uuid4()) + os.path.splitext(i.filename)[1])))

    zip_filename = f"{imagesDir}/{ranFolder}.zip"
    with zipfile.ZipFile(zip_filename, "w") as zip:
        for image_name in os.listdir(imagesFolder):
            zip.write(os.path.join(imagesFolder, image_name), arcname=image_name)

    shutil.rmtree(os.path.join(imagesDir, ranFolder))
    return zipRef


def sendZipImages(imagesRef):
    image_zip = imagesDir + '/' + imagesRef

    response = send_file(
        image_zip,
        mimetype='application/zip',
        as_attachment=True,
        download_name=imagesRef
    )
    return response


def deleteZipImages(zip):
    os.remove(os.path.join(imagesDir, zip))