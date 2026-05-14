"""
API Routes for User Management Microservice
"""
from flask import Blueprint, request, jsonify
from app.models import db, UserPreference
import uuid

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/<user_id>/preferences', methods=['GET'])
def get_user_preferences(user_id):
    """Get user preferences by user ID"""
    try:
        pref = UserPreference.query.filter_by(user_id=user_id).first()
        if not pref:
            # Return default preferences if user preferences don't exist
            return jsonify({
                'userId': user_id,
                'preferAccessibleRoutes': False,
                'preferFewestTransfers': False,
                'favoriteRoutes': [],
                'recentSearches': []
            }), 200
        
        return jsonify({
            'userId': pref.user_id,
            'preferAccessibleRoutes': pref.prefer_accessible_routes,
            'preferFewestTransfers': pref.prefer_fewest_transfers,
            'favoriteRoutes': pref.favorite_routes.split(',') if pref.favorite_routes else [],
            'recentSearches': []
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@users_bp.route('/<user_id>/preferences', methods=['POST'])
def update_user_preferences(user_id):
    """Update user preferences"""
    try:
        data = request.get_json()
        
        pref = UserPreference.query.filter_by(user_id=user_id).first()
        if not pref:
            pref = UserPreference(
                id=str(uuid.uuid4()),
                user_id=user_id,
                prefer_accessible_routes=data.get('preferAccessibleRoutes', False),
                prefer_fewest_transfers=data.get('preferFewestTransfers', False),
                favorite_routes=','.join(data.get('favoriteRoutes', []))
            )
            db.session.add(pref)
        else:
            pref.prefer_accessible_routes = data.get('preferAccessibleRoutes', pref.prefer_accessible_routes)
            pref.prefer_fewest_transfers = data.get('preferFewestTransfers', pref.prefer_fewest_transfers)
            if 'favoriteRoutes' in data:
                pref.favorite_routes = ','.join(data['favoriteRoutes'])
        
        db.session.commit()
        
        return jsonify({
            'userId': pref.user_id,
            'preferAccessibleRoutes': pref.prefer_accessible_routes,
            'preferFewestTransfers': pref.prefer_fewest_transfers,
            'favoriteRoutes': pref.favorite_routes.split(',') if pref.favorite_routes else []
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@users_bp.route('/<user_id>/preferences/favorite-routes/<route_id>', methods=['POST'])
def add_favorite_route(user_id, route_id):
    """Add a route to user's favorites"""
    try:
        pref = UserPreference.query.filter_by(user_id=user_id).first()
        if not pref:
            pref = UserPreference(
                id=str(uuid.uuid4()),
                user_id=user_id,
                favorite_routes=route_id
            )
            db.session.add(pref)
        else:
            favorites = pref.favorite_routes.split(',') if pref.favorite_routes else []
            if route_id not in favorites:
                favorites.append(route_id)
                pref.favorite_routes = ','.join(favorites)
        
        db.session.commit()
        
        return jsonify({
            'userId': pref.user_id,
            'preferAccessibleRoutes': pref.prefer_accessible_routes,
            'preferFewestTransfers': pref.prefer_fewest_transfers,
            'favoriteRoutes': pref.favorite_routes.split(',') if pref.favorite_routes else []
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
