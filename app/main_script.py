import os
from ml_component.ml_processor import process_csv
from flask_api.routes import  tenant_collection, project_metadata_collection , Tenant, ProjectMetadata
from uploads.s3bucket import S3Uploader , unique_filename
model_file_path = 'model'
bucket_name = 'storedmodel'

def main():
    try:
        tenant = Tenant(name=unique_filename)
        csv_file_location = os.environ.get('LOCAL_CSV_FILE', "C:/Users/rohit/OneDrive/Desktop/mlaws/app/melb_data.csv")
        target_column = os.environ.get('TARGET_COLUMN',"Price" )

        model, evaluation_results = process_csv(csv_file_location, target_column)

        project_metadata = ProjectMetadata(
            tenant=tenant,
            local_csv_location=csv_file_location,
            s3_model_location="s3://bucket/storedmodel",
            model_evaluation_results=f"Evaluation: {evaluation_results}% accuracy"
        )

        tenant_collection.insert_one({'name': tenant.name
                                      })

        project_metadata_collection.insert_one({
            'tenant': project_metadata.tenant.name,
            'local_csv_location': project_metadata.local_csv_location,
            's3_model_location': project_metadata.s3_model_location,
            'model_evaluation_results': project_metadata.model_evaluation_results
        })


        print("Tenant Record:", tenant.__dict__)
        print("Project Metadata Record: Fetch from MongoDB")
        cursor = project_metadata_collection.find()
        for document in cursor:
            print(document)

        s3_uploader = S3Uploader(bucket_name)
        s3_uploader.upload_model(model_file_path)

    except Exception as e:
        print(f"Error: {str(e)}")




if __name__ == "__main__":
    main()

