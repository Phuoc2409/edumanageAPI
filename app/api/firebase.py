from flask import Flask, request, jsonify, Blueprint
from flask import Blueprint, jsonify, request

from app.services.firebase_service import upload_notification_to_firebase, update_notification_status
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
        return jsonify({'error': str(e)}), 5002

@firebase_bp.route('/api/update_status', methods=['PUT'])
def update_status():
    try:
        data = request.get_json()
        # Ensure required data is provided
        if not data or 'notification_id' not in data or 'status' not in data:
            return jsonify({"error": "Missing notification_id or status"}), 400
        
        notification_id = data['notification_id']
        new_status = data['status']
        
        # Update status
        result = update_notification_status(notification_id, new_status)
        if result:
            return jsonify({"message": "Notification status updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500