#!/usr/bin/env python3

import tempfile
import glob
import logging
import os
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
import boto3

bucket = 'kutny-kodi'
fileSizeLimit = 1024 * 1024

rootDir = '/home/osmc'

dirs = [
    '/Movies',
    '/TV Shows',
]

files = [
    '/.kodi/addons/plugin.video.stream-cinema-2-release/resources/settings.xml',
    '/.kodi/addons/plugin.video.stream-cinema/resources/settings.xml',
    '/.kodi/userdata/addon_data/plugin.video.stream-cinema-2-release/settings.xml',
    '/.kodi/userdata/addon_data/plugin.video.stream-cinema/settings.xml',
    '/.kodi/userdata/sources.xml',
    '/.kodi/userdata/favourites.xml',
    '/.kodi/userdata/guisettings.xml',
]

def addDirToZip(relativeDirToAdd: str, myZipFile: ZipFile):
    dirStr = rootDir + relativeDirToAdd

    logging.info('Adding directory {}'.format(dirStr))

    for filePathStr in glob.iglob(dirStr + '/**/*.*', recursive=True):
        filePath = Path(filePathStr)

        if os.path.getsize(str(filePath)) > fileSizeLimit:
            logging.debug('Skipping too large file {}'.format(filePath))
            continue

        logging.debug('Adding file {}'.format(filePath))

        myZipFile.write(str(filePath), str(filePath.relative_to(Path(rootDir))), ZIP_DEFLATED)

def addFileToZip(relativeFileToAdd: str, myZipFile: ZipFile):
    filePathStr = rootDir + relativeFileToAdd

    logging.info('Adding file {}'.format(filePathStr))

    myZipFile.write(filePathStr, str(Path(filePathStr).relative_to(Path(rootDir))), ZIP_DEFLATED)

def createZipFile() -> Path:
    timeName = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backupFilePath = tempfile.gettempdir() + "/kodi_backup_{}.zip".format(timeName)

    logging.info('Creating {}'.format(backupFilePath))

    myZipFile = ZipFile(backupFilePath, "w")

    for dir in dirs:
        addDirToZip(dir, myZipFile)

    for file in files:
        addFileToZip(file, myZipFile)

    myZipFile.close()

    return Path(backupFilePath)

def uploadFile(backupFilePath: Path):
    logging.info('Uploading back file {} to S3'.format(backupFilePath))

    s3_client = boto3.client('s3')
    s3_client.upload_file(str(backupFilePath), bucket, backupFilePath.name)

    logging.info('Upload complete')

def main():
    logging.basicConfig(level=logging.INFO)

    backupFilePath = createZipFile()
    uploadFile(backupFilePath)

if __name__ == '__main__':
    main()
