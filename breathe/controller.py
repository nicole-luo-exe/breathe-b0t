from main import app

from pprint import pprint
from flask import request

from api.dialogflow_api import detect_intent_via_text, detect_intent_via_event
from api.telegram_api import send_message
from beans.session import Session
from beans.user import User
from cache import get_current_session
from command_handlers import COMMAND_HANDLERS, handle_invalid_command
from intent_handlers import INTENT_HANDLERS, handle_invalid_intent
from main import app
from utils import \
    get_user_from_request, \
    get_user_input_from_request, \
    default_if_blank, \
    is_not_blank, \
    get_user_command_from_request

@app.route('/webhook', methods=['POST'])
def webhook():
    req_body = request.get_json()

    user = get_user_from_request(req_body)
    user_input = get_user_input_from_request(req_body)
    session = get_current_session(user)

    intent_result = __process_dialogflow_input(user, session, user_input)

    send_message(user, 'random_state', 'random_Session_id', '')

    return ''

# Calls Dialogflow API to trigger an intent match
def __process_dialogflow_input(user: User, session: Session, user_input):
    intent_result = detect_intent_via_text(session.id, user_input)
    pprint(intent_result)

    return intent_result