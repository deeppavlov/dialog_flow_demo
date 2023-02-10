from typing import Callable

from dff.script import Context, Actor

from . import utils

def has_intent(label: tuple) -> Callable:
    def has_intent_inner(ctx: Context, actor: Actor) -> bool:
        if ctx.validation:
            return False

        return label in ctx.misc.get(utils.DNNC_INTENTS, [])

    return has_intent_inner


def slots_filled(slots: list) -> Callable:
    def slots_filled_inner(ctx: Context, actor: Actor) -> bool:
        if ctx.validation:
            return False

        return all([slot in ctx.misc[utils.SLOTS] for slot in slots])
    
    return slots_filled_inner
