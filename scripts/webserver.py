from flask import Blueprint, render_template, request, redirect, url_for, session


from scripts.bandersnatch_utils import mirror_package
from scripts.validation import is_valid_package_name
from scripts.file_utils import get_latest_file, delete_file
from scripts.archive_utils import create_archive
from scripts.logger import configure_logger, logger

# Configure rotating logger
configure_logger(log_file="./webserver.log")  # only once at startup
# Logs are written to 'webserver.log' and rotated when they exceed 1MB (up to 5 backups)

# Constants for directories and path string replacements
SOURCE_FOLDER = "/mnt/python/data/changes/"  # Bandersnatch output folder
OUTPUT_FOLDER = "/mnt/python/data/upload/"  # Folder for modified and archived files

# Define a Flask blueprint for modular route handling
bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Route handler for the main page.

    - On POST: validates the package name, mirrors it using bandersnatch,
      stores results in session, and redirects.
    - On GET: processes latest file, creates archive, and shows results.

    Returns:
        Rendered HTML template with result message.
    """
    logger.debug("[WEB] index() called")

    if request.method == 'POST':
        # Get the package name from the form
        input_text = request.form['inputText']
        logger.info(f"Received input text: {input_text}")

        # Validate the package name format
        if not is_valid_package_name(input_text):
            logger.warning("Invalid package name")
            return render_template('index.html', result="Invalid package name")

        try:
            # Start the mirroring process
            logger.info("Starting mirror_package")
            result = mirror_package(input_text)
            logger.info("mirror_package completed successfully")

            # Store data in session for use after redirect
            session['mirror_result'] = result
            session['input_package'] = input_text

            # Redirect to GET route (Post/Redirect/Get pattern)
            return redirect(url_for('index.index'))

        except Exception as e:
            # Log exception and render the error message
            logger.exception("Error during mirror_package")
            return render_template('index.html', result=str(e))

    try:
        # Handle GET request (after redirect or direct page load)
        logger.debug("Starting GET block")
        logger.debug(f"OUTPUT_FOLDER: {SOURCE_FOLDER}")

        # Retrieve the latest file from the source folder
        latest_file = get_latest_file(SOURCE_FOLDER)
        logger.info(f"Latest file found: {latest_file}")

        # Retrieve the input package name from session
        input_package = session.pop('input_package', None)

        # Create archive from the latest file and package name
        archive_path = create_archive(
            latest_file,
            input_package,
            OUTPUT_FOLDER
        )
        logger.info(f"Archive created at: {archive_path}")

        #delete the lastest file
        delete_file(latest_file)

        # Retrieve mirror result from session
        mirror_result = session.pop('mirror_result', '')

        # Build HTML result message for rendering
        result_message = (
            f"{mirror_result}<br><br>"
            f"Latest file: {latest_file}<br>"
            f"Archive created at: {archive_path}"
        )


        return render_template('index.html', result=result_message)

    except Exception as e:
        # Catch and log any errors during GET processing
        logger.exception("Error in GET block")
        return render_template('index.html', result=str(e))
