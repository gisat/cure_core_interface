from flask import Blueprint, render_template, request
from pathlib import Path

main = Blueprint('main', __name__)


@main.route("/")
def index():
    """Show documentation"""

    # open readme
    with open(Path(main.root_path).parent.parent / 'README.md', 'r') as md:
        # read file
        content = md.read()
        # convert to HTML
        return render_template('main.html', title='Documentation', markdown=content)

@main.route("/test")
def test():
    """Debug"""
    test = request.args.get('test', None)
    return render_template('test.html', title='Test', text=test)




