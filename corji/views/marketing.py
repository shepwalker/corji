"""Random, likely static, views that don't actually consist within the app."""

from flask import (
    Blueprint,
    render_template
)

from corji import (
    settings
)

marketing_blueprint = Blueprint('marketing', __name__,
                                template_folder='templates')


@marketing_blueprint.route("/", methods=['GET'])
def about():
    """Much hype.  Very disruptive.  Such blurb."""
    return render_template('html/about.html',
                           google_analytics_id=settings.Config.GOOGLE_ANALYTICS_ID)
