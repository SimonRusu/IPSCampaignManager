import pathlib
import shutil
import os
import zipfile
from flask import send_file
from uuid import uuid4
from werkzeug.utils import secure_filename

images_directory = 'db/campaign_images'

def generateZipWithImages(images):
    ranFolder = str(uuid4())
    zipRef = ranFolder + '.zip'
    imagesFolder = os.path.join(pathlib.Path(__file__).parent.parent.resolve(), images_directory, ranFolder)
    os.makedirs(imagesFolder)

    for i in images:
        i.save(os.path.join(imagesFolder, secure_filename(str(uuid4()) + os.path.splitext(i.filename)[1])))

    zip_filename = f"{images_directory}/{ranFolder}.zip"
    with zipfile.ZipFile(zip_filename, "w") as zip:
        for image_name in os.listdir(imagesFolder):
            zip.write(os.path.join(imagesFolder, image_name), arcname=image_name)

    shutil.rmtree(os.path.join(images_directory, ranFolder))
    return zipRef


def sendZipWithImages(imagesRef):
    image_zip = images_directory + '/' + imagesRef

    response = send_file(
        image_zip,
        mimetype='application/zip',
        as_attachment=True,
        download_name=imagesRef
    )
    return response