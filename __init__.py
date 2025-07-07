from flask import Blueprint, render_template, request, jsonify
from CTFd.plugins import register_plugin_assets_directory, register_plugin_script
from CTFd.utils import get_config
from CTFd.utils.decorators import admins_only, authed_only
from CTFd.models import db, Teams, Submissions, Solves
from sqlalchemy import Column, Integer, Boolean, DateTime
import random
from CTFd.utils.scoreboard import get_standings
from datetime import datetime

# -----------------------------
# Database model for config
# -----------------------------
class StatusConfig(db.Model):
    __tablename__ = "status_page_config"
    id = Column(Integer, primary_key=True)
    nb_teams = Column(Integer, nullable=False, default=20)
    show_stats = Column(Boolean, nullable=False, default=False)
    show_timer = Column(Boolean, nullable=False, default=False)
    end_time = Column(DateTime, nullable=True)
    show_support = Column(Boolean, nullable=False, default=False)
    support_percent = Column(Integer, nullable=False, default=0)
    support_admins_online = Column(Integer, nullable=False, default=0)

# Create table and initial config
def create_status_config():
    # StatusConfig.__table__.drop(db.engine)  # Uncomment to reset table during dev
    db.create_all()
    config = StatusConfig.query.first()
    if not config:
        config = StatusConfig(
            nb_teams=20,
            show_stats=False,
            show_timer=False,
            end_time=None,
            show_support=False,
            support_percent=0,
            support_admins_online=0
        )
        db.session.add(config)
        db.session.commit()

# -----------------------------
# Main plugin load function
# -----------------------------
def load(app):
    create_status_config()

    status_bp = Blueprint(
        'status_page',
        __name__,
        template_folder='templates',
        static_folder='assets',
        url_prefix='/plugins/status-page'
    )

    # -----------------------------
    # User-facing status page
    # -----------------------------
    @status_bp.route('/user')
    @authed_only
    def status_user():
        event_name = get_config('ctf_name')
        config = StatusConfig.query.first()
        nb_teams = config.nb_teams if config else 20
        return render_template('user_viewer.html', event_name=event_name, nb_teams=nb_teams)

    # -----------------------------
    # Admin configuration page
    # -----------------------------
    @status_bp.route('/admin')
    @admins_only
    def status_admin():
        event_name = get_config('ctf_name')
        return render_template('admin_viewer.html', event_name=event_name)

    # -----------------------------
    # Save admin settings
    # -----------------------------
    @status_bp.route('/admin/save', methods=['POST'])
    @admins_only
    def save_status_config():
        data = request.get_json()
        nb_teams = int(data.get("nb_teams", 20))
        show_stats = data.get("show_stats", False)
        show_timer = data.get("show_timer", False)
        end_time_str = data.get("end_time", None)
        show_support = data.get("show_support", False)
        support_percent = int(data.get("support_percent", 0))
        support_admins_online = int(data.get("support_admins_online", 0))

        config = StatusConfig.query.first()
        if config:
            config.nb_teams = nb_teams
            config.show_stats = show_stats
            config.show_timer = show_timer
            config.show_support = show_support
            config.support_percent = support_percent
            config.support_admins_online = support_admins_online
            if end_time_str:
                config.end_time = datetime.fromisoformat(end_time_str)
            else:
                config.end_time = None
        else:
            config = StatusConfig(
                nb_teams=nb_teams,
                show_stats=show_stats,
                show_timer=show_timer,
                show_support=show_support,
                support_percent=support_percent,
                support_admins_online=support_admins_online,
                end_time=datetime.fromisoformat(end_time_str) if end_time_str else None
            )
            db.session.add(config)
        db.session.commit()
        return jsonify({"success": True})

    # -----------------------------
    # API: Get settings for admin
    # -----------------------------
    @status_bp.route('/api/settings')
    @admins_only
    def get_status_config():
        config = StatusConfig.query.first()
        return jsonify({
            "nb_teams": config.nb_teams if config else 20,
            "show_stats": config.show_stats if config else False,
            "show_timer": config.show_timer if config else False,
            "show_support": config.show_support if config else False,
            "support_percent": config.support_percent if config else 0,
            "support_admins_online": config.support_admins_online if config else 0,
            "end_time": config.end_time.isoformat() if config and config.end_time else None
        })

    # -----------------------------
    # API: User random scoreboard
    # -----------------------------
    @status_bp.route('/api/user/top')
    @authed_only
    def get_top_teams():
        config = StatusConfig.query.first()
        nb_teams = config.nb_teams if config else 20

        standings = get_standings(admin=False)
        teams = standings[:nb_teams]
        random.shuffle(teams)

        team_data = [{"id": t.account_id, "name": t.name} for t in teams]
        return jsonify(team_data)

    # -----------------------------
    # API: User global event stats / support / time
    # -----------------------------
    @status_bp.route('/api/user/stats')
    @authed_only
    def get_user_stats():
        config = StatusConfig.query.first()
        show_stats = config.show_stats if config else False

        valid_team_ids = [team.id for team in Teams.query.filter(Teams.banned == False, Teams.hidden == False).all()]

        correct_subs = Solves.query.filter(Solves.team_id.in_(valid_team_ids)).count()
        incorrect_subs = Submissions.query.filter(
            Submissions.team_id.in_(valid_team_ids),
            Submissions.provided == False
        ).count()

        total_subs = correct_subs + incorrect_subs

        success_rate = (correct_subs / total_subs * 100) if total_subs > 0 else 0
        failure_rate = (incorrect_subs / total_subs * 100) if total_subs > 0 else 0

        return jsonify({
            "show_stats": show_stats,
            "total_subs": total_subs,
            "correct_subs": correct_subs,
            "incorrect_subs": incorrect_subs,
            "success_rate": round(success_rate, 1),
            "failure_rate": round(failure_rate, 1),
            "show_timer": config.show_timer,
            "end_time": config.end_time.isoformat() if config.end_time else None,
            "show_support": config.show_support,
            "support_percent": config.support_percent,
            "support_admins_online": config.support_admins_online
        })



    # -----------------------------
    # Register blueprint & assets
    # -----------------------------
    app.register_blueprint(status_bp)
    register_plugin_assets_directory(app, base_path='/plugins/status-page/assets')
    register_plugin_script('/plugins/status-page/assets/settings.js')
