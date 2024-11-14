from flask import Flask, request, jsonify, Blueprint
from flask import Blueprint, jsonify, request

from app.services.firebase_service import upload_notification_to_firebase
firebase_bp = Blueprint('firebase', __name__)

@firebase_bp.route('/upload_notification', methods=['POST'])
def upload_data():
    try:
        # Lấy dữ liệu từ request body
        data = request.get_json()

        # Gọi service để upload dữ liệu lên Firebase
        firebase_id = upload_notification_to_firebase(data)

        return jsonify({
            'message': 'Dữ liệu đã được tải lên Firebase!',
            'id': firebase_id
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500