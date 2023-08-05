import firebase_admin
from firebase_admin import credentials, firestore
import os

firebase_admin_config = {
  "type": "service_account",
  "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
  "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
  "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace(r'\n', '\n'),
  "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
  "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL"),
  "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(firebase_admin_config)
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_document(collection_name: str, document_id: str, data: dict):
    try:
        # Get the collection reference
        collection_ref = db.collection(collection_name)

        # Add the document to the collection with the specified document_id
        collection_ref.document(document_id).set(data)

        return {"success": True, "message": "Document added successfully."}
    except Exception as e:
        return {"success": False, "message": str(e)}
    

def update_document(collection_name: str, document_id: str, data: dict):
    try:
        # Get the document reference
        doc_ref = db.collection(collection_name).document(document_id)
        
        if (not doc_ref.get().exists):
            doc_ref.set(data)
        # Update the document with the specified data
        doc_ref.update(data)

        return {"success": True, "message": "Document updated successfully."}
    except Exception as e:
        return {"success": False, "message": str(e)}
    
def delete_document(collection_name: str, document_id: str):
    try:
        # Get the document reference
        doc_ref = db.collection(collection_name).document(document_id)

        # Delete the document
        doc_ref.delete()

        return {"success": True, "message": "Document deleted successfully."}
    except Exception as e:
        return {"success": False, "message": str(e)}
