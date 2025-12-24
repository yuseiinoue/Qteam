"""
イベントに関するエンドポイント
"""
import logging
from flask import Blueprint, jsonify, request
from services.event_service import EventService

event_bp = Blueprint('event', __name__)
event_service = EventService()
logger = logging.getLogger(__name__)

@event_bp.route('/events', methods=['GET'])
def get_events():
    """イベント一覧を取得（フィルター対応）"""
    try:
        # クエリパラメータを取得
        month = request.args.get('month')
        area = request.args.get('area')

        # フィルター適用
        if month:
            try:
                month_value = int(month)
            except (TypeError, ValueError):
                return jsonify({'error': '月は1〜12の範囲で指定してください'}), 400

            if not 1 <= month_value <= 12:
                return jsonify({'error': '月は1〜12の範囲で指定してください'}), 400

            events = event_service.get_events_by_month(month_value)
        elif area:
            events = event_service.get_events_by_area(area)
        else:
            events = event_service.get_all_events()

        return jsonify(events)
    except Exception:
        logger.exception('Failed to get events')
        return jsonify({'error': 'イベントの取得に失敗しました'}), 500

@event_bp.route('/events/search', methods=['GET'])
def search_events():
    """イベントを検索"""
    try:
        keyword = request.args.get('q', '')
        if not keyword:
            return jsonify({'error': 'キーワードが指定されていません'}), 400

        events = event_service.search_events(keyword)
        return jsonify(events)
    except Exception:
        logger.exception('Failed to search events')
        return jsonify({'error': 'イベントの検索に失敗しました'}), 500
