import sys
import re
import shutil
from pathlib import Path


JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
MY_OTHER = []
ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []
DOC_DOCUMENT = []
DOCX_DOCUMENT = []
TXT_DOCUMENT = []
PDF_DOCUMENT = []
XLSX_DOCUMENT = []
PPTX_DOCUMENT = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ZIP_ARCHIVES,
    'GZ': GZ_ARCHIVES,
    'TAR': TAR_ARCHIVES,
    'DOC': DOC_DOCUMENT,
    'DOCX': DOCX_DOCUMENT,
    'TXT': TXT_DOCUMENT,
    'PDF': PDF_DOCUMENT,
    'XLSX': XLSX_DOCUMENT,
    'PPTX': PPTX_DOCUMENT,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()  # suffix[1:] -> .jpg -> jpg

def scan(folder: Path):
    for item in folder.iterdir():
        # Робота з папкою
        if item.is_dir():  # перевіряємо чи обєкт папка
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        # Робота з файлом
        extension = get_extension(item.name)  # беремо розширення файлу
        full_name = folder / item.name  # беремо повний шлях до файлу
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)  # .mp4, .mov, .avi
                MY_OTHER.append(full_name)





CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()


def normalize(name: str) -> str:
    translate_name = re.sub(r'\W', '_', name.translate(TRANS))
    return translate_name






def handle_media(file_name: Path, target_folder: Path):
    # target_folder.mkdir(exist_ok=True, parents=True)
    # file_name.replace(target_folder / normalize(file_name.name))

    target_folder.mkdir(exist_ok=True, parents=True)
    normalized_name = normalize(file_name.stem) + file_name.suffix
    file_name.replace(target_folder / normalized_name)

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()


def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
        
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3_AUDIO')
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG_AUDIO')
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV_AUDIO')
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR_AUDIO')

    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI_VIDEO')
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4_VIDEO')
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV_VIDEO')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV_VIDEO')

    for file in DOC_DOCUMENT:
        handle_media(file, folder / 'documents' / 'DOC_DOCUMENT')
    for file in DOCX_DOCUMENT:
        handle_media(file, folder / 'documents' / 'DOCX_DOCUMENT')
    for file in TXT_DOCUMENT:
        handle_media(file, folder / 'documents' / 'TXT_DOCUMENT')
    for file in PDF_DOCUMENT:
        handle_media(file, folder / 'documents' / 'PDF_DOCUMENT')
    for file in XLSX_DOCUMENT:
        handle_media(file, folder / 'documents' / 'XLSX_DOCUMENT')
    for file in PPTX_DOCUMENT:
        handle_media(file, folder / 'documents' / 'PPTX_DOCUMENT')

    for file in ZIP_ARCHIVES:
        handle_archive(file, folder /'archives'/ 'ZIP_ARCHIVES')
    for file in GZ_ARCHIVES:
        handle_archive(file, folder /'archives'/ 'GZ_ARCHIVES')
    for file in TAR_ARCHIVES:
        handle_archive(file, folder /'archives'/ 'TAR_ARCHIVES')

    for file in MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')

    for folder in FOLDERS[::-1]:
        # Видаляємо пусті папки після сортування
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')


def start():
    if sys.argv[1]:
       folder_process = Path(sys.argv[1])
       main(folder_process)



