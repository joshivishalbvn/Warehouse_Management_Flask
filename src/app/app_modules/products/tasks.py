import os
import requests
from app import db
import pandas as pd
from celery import shared_task
from app.app_modules.company.models import Company
from .models import  CSVFile, Product, ProductCase, ProductImage
from app.helper.utils import generate_barcode,save_image_from_given_link

@shared_task()
def import_product_from_csv(csv_file_id):
    try:
        context = {"messages": []}
        csv_file_obj = CSVFile.query.get(csv_file_id)
        upload_folder = os.path.join('app','static', 'uploads', 'csv_files')
        file_path = os.path.join(upload_folder, csv_file_obj.csv_file_url)
        df = pd.read_excel(file_path)
        df = df.fillna('')
        file_data = df.to_dict(orient='records')

        for record in file_data:
            # <--------------------product details---------------------->
            company = Company.query.filter_by(name=record["COMPANY"]).first()
            product_obj = Product.query.filter_by(company_id=company.id, name=record["PRODUCT_NAME"]).first()
            if product_obj is None:
                product_obj = Product(company_id=company.id, name=record["PRODUCT_NAME"])
            product_obj.code = record["CODE"]
            product_obj.status = Product.ACTIVE
            db.session.add(product_obj)
            db.session.commit()

            # stock_obj, _ = Stock.objects.get_or_create(
            #     product = product_obj,
            #     company = company,
            # )
            # stock_obj.save()
            
            # <--------------------end of product details--------------->
            try:
                image_key = 'IMAGE_URL'
                image_url = record.get(image_key)
                
                if image_url:
                    response = requests.get(
                        image_url,
                        timeout=10,
                        headers={
                            "User-Agent": (
                                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                " Chrome/107.0.0.0 Safari/537.36"
                            )
                        }
                    )
                    
                    if response.status_code == 200:
                        file_path = save_image_from_given_link(image_url, response.content)  # Modify save_image to accept image content
                        product_image = ProductImage(image_url=file_path, product_id=product_obj.id)
                        db.session.add(product_image)
                        db.session.commit()
                    else:
                        print(f"Failed to download image: {image_url}, status code: {response.status_code}")
                
            except Exception as e:
                import traceback
                traceback.print_exc()

            # <---------------quantity details--------------------------->
            try:
                max = list(record.keys())[-1].split("_")[-1]
                for i in range(1, int(max)+1):
                    weight_key = f"CASE_WEIGHT_{i}"
                    qty_key = f"CASE_PRODUCT_QUANTITY_{i}"
                    volume_key = f"CUBIC_METER_VOLUME_{i}"

                    weight = record.get(weight_key)
                    quantity = record.get(qty_key)
                    volume = record.get(volume_key)

                    if type(weight) == int and type(quantity) == int and type(volume) == int:
                        product_case_obj = ProductCase(
                            weight=weight,
                            quantity=quantity,
                            product_id=product_obj.id,
                            cubic_meter_volume=volume
                        )
                        db.session.add(product_case_obj)
                        db.session.commit()

                    
                    else:
                        pass
            except:
                import traceback
                traceback.print_exc()
                pass
            # <---------------end of quantity details---------------------->

            # <---------------------Barcode Data-------------------------------->
            try:
                    product_id=product_obj.id,
                    number=record.get("BARCODE_NUMBER")

                    try:
                        generate_barcode(number,product_id)
                    except Exception:
                        pass
            except:
                import traceback
                traceback.print_exc()
                pass
            # <---------------------End Of Barcode Data--------------------------->

    except Exception as e:
        import traceback
        traceback.print_exc()
        context['exceptions_raised'] = e