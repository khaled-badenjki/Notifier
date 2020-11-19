def process_text(text, extra_params, is_dynamic):
    if is_dynamic:
        for extra_param in extra_params:
            text = text.replace(extra_param["key"], extra_param["value"])
    return text
