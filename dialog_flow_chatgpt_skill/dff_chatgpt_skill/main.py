from dff.script import RESPONSE, TRANSITIONS, LOCAL, PRE_TRANSITIONS_PROCESSING, PRE_RESPONSE_PROCESSING
from dff.script import Message
from dff.script import conditions as cnd
from dff.script import labels as lbl

from . import conditions as loc_cnd
from . import response as loc_rsp
from . import processing as loc_prc


script = {
    "general_flow": {
        LOCAL: {
            TRANSITIONS: {
                ("form_flow", "ask_item", 1.0): loc_cnd.has_intent(("home", "order")),
                ("chitchat_flow", "chitchat_init", 0.8): cnd.true()
            }
        },
        "start_node": {
            RESPONSE: Message(text=""),
        },
        "fallback_node": {
            RESPONSE: Message(text="Cannot recognize your query. Type ok to continue."),
        }
    },
    "chitchat_flow": {
        LOCAL: {
            TRANSITIONS: {
                ("form_flow", "ask_item", 1.0): loc_cnd.has_intent(("home", "order")),
                lbl.repeat(0.8): cnd.true()
            }
        },
        "init_chitchat": {
            RESPONSE: Message(text="Welcome to 'Book Lovers Paradise'! Ask us anything you would like to know."),
            TRANSITIONS: {
                ("chitchat_flow", "chitchat"): cnd.true()
            }
        },
        "chitchat": {
            PRE_RESPONSE_PROCESSING: {
                "1": loc_prc.generate_response()
            },
            TRANSITIONS: {
                lbl.repeat(): cnd.true()
            },
            RESPONSE: loc_rsp.choose_response
        },
    },
    "form_flow": {
        LOCAL: {
            TRANSITIONS: {
                ("chitchat_flow", "chitchat", 1.2): cnd.any([loc_cnd.has_intent(("meta", "cancel")), loc_cnd.has_intent(("meta", "no"))]),
                lbl.repeat(0.8): cnd.true()
            }
        },
        "ask_item": {
            RESPONSE: Message(text="Which books would you like to order? Please, separate the titles by commas."),
            PRE_TRANSITIONS_PROCESSING: {
                "1": loc_prc.extract_item()
            },
            TRANSITIONS: {
                lbl.forward(): loc_cnd.slots_filled(["items"])
            }
        },
        "ask_delivery": {
            RESPONSE: Message(text="Which delivery method would you like to use? We currently offer pickup or home delivery."),
            PRE_TRANSITIONS_PROCESSING: {
                "1": loc_prc.extract_delivery()
            },
            TRANSITIONS: {
                lbl.forward(): loc_cnd.slots_filled(["delivery"])
            }
        },
        "ask_address": {
            RESPONSE: Message(text="Please, enter your address. If you chose pickup as delivery method, please, ignore."),
            PRE_TRANSITIONS_PROCESSING: {
                "1": loc_prc.extract_address()
            },
            TRANSITIONS: {
                lbl.forward(): cnd.true()
            }
        },
        "ask_payment_method": {
            RESPONSE: Message(text="Please, enter the payment method you would like to use: cash or credit card."),
            PRE_TRANSITIONS_PROCESSING: {
                "1": loc_prc.extract_payment_method()
            },
            TRANSITIONS: {
                ("chitchat_flow", "chitchat"): loc_cnd.slots_filled(["payment_method"])
            }
        }
    }
}