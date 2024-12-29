from io import BytesIO
import os
import uuid
from flask import request
from werkzeug.utils import secure_filename
from app import db
from app.app_modules.company.models import Company
from app.app_modules.products.forms import BarcodeCreateFromCSVForm
from app.app_modules.products.models import Barcode, CSVFile, Product, ProductCase, ProductImage
from app.app_modules.stocks.models import StockHistory
from app.app_modules.customers.models import CustomerDocuments

def save_image(image):
    upload_folder = os.path.join('app','static', 'uploads', 'product_images')
    upload_folder_root = os.path.join('uploads', 'product_images')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filename = secure_filename(image.filename)
    file_path = os.path.join(upload_folder, filename)
    upload_folder_path = os.path.join(upload_folder_root, filename)
    image.save(file_path)
    return upload_folder_path

def save_document(attachment):
    upload_folder = CustomerDocuments.DOCUMENTS_FILE_PATH
    upload_folder_root = CustomerDocuments.DOCUMENTS_FILE_ROOT_PATH
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filename = secure_filename(attachment.filename)
    file_path = os.path.join(upload_folder, filename)
    upload_folder_path = os.path.join(upload_folder_root, filename)
    attachment.save(file_path)
    return upload_folder_path

from io import BytesIO
from barcode import Code39
from barcode.writer import ImageWriter
import uuid
import os
from app import db
from app.app_modules.products.models import Barcode

def generate_barcode(barcode_number, product_id,barcode_obj=None):
    barcode_number = str(barcode_number)
    buffer = BytesIO()
    try:
        my_code = Code39(barcode_number, writer=ImageWriter(), add_checksum=False)
        my_code.write(buffer)
        buffer.seek(0)

        file_name = f"{str(uuid.uuid4())}.png"
        upload_folder = os.path.join('app', 'static', 'uploads', 'barcodes')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, file_name)

        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())

        if barcode_obj:
            barcode_obj.number=barcode_number,
            barcode_obj.code_url=file_name,
            barcode_obj.product_id=product_id
            db.session.add(barcode_obj)
            db.session.commit()
        else:
            barcode = Barcode(
                number=barcode_number,
                code_url=file_name,
                product_id=product_id
            )
            db.session.add(barcode)
            db.session.commit()
        return True

    except Exception as e:
        print("Error generating or saving barcode:", e)
        import traceback
        traceback.print_exc()
        return None

def update_barcode(barcode_id,barcode_number):
    barcode_obj = Barcode.query.get_or_404(barcode_id)
    barcode_folder = os.path.join('app', 'static', 'uploads', 'barcodes')
    file_name = barcode_obj.code_url
    old_file_path = os.path.join(barcode_folder, file_name)
    if os.path.exists(old_file_path):
        os.remove(old_file_path)

    generate_barcode(barcode_number,barcode_obj.product_id,barcode_obj)

def update_document(doc_id,attachment):
    doc_obj = CustomerDocuments.query.get_or_404(doc_id)
    attachment_path = CustomerDocuments.DOCUMENTS_FILE_PATH
    file_name = doc_obj.attachment.split("/")[-1]
    old_file_path = os.path.join(attachment_path, file_name)
    if os.path.exists(old_file_path):
        os.remove(old_file_path)
    return save_document(attachment)

def delete_document(doc_id):
    doc_obj = CustomerDocuments.query.get_or_404(doc_id)
    attachment_path = CustomerDocuments.DOCUMENTS_FILE_PATH
    file_name = doc_obj.attachment.split("/")[-1]
    old_file_path = os.path.join(attachment_path, file_name)
    if os.path.exists(old_file_path):
        os.remove(old_file_path)

def save_csv(csv_file):
    upload_folder = os.path.join('app','static', 'uploads', 'csv_files')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filename = secure_filename(csv_file.filename)
    file_path = os.path.join(upload_folder, filename)
    upload_folder_path = os.path.join(upload_folder, filename)
    csv_file.save(file_path)
    return filename



def save_image_from_given_link(image_url, content):
    # Define your file path and saving logic
    file_name = os.path.basename(image_url)
    upload_folder = os.path.join('app','static', 'uploads', 'product_images')
    file_path = os.path.join(upload_folder, file_name)
    upload_folder_root = os.path.join('uploads', 'product_images')
    upload_folder_path = os.path.join(upload_folder_root, file_name)
    with open(file_path, 'wb') as f:
        f.write(content)
    
    return upload_folder_path


def update_history_obj(stock_history_id):
    print('\033[91m'+'stock_history_id: ' + '\033[92m', stock_history_id)
    # instance = StockHistory.query.get(stock_history_id)
    # print('\033[91m'+'instance: ' + '\033[92m', instance)