from mercurio import engine


def test_dict_from_readline_with_valid_input():
    value = "target=something"
    result = engine._dict_from_readline(value)
    assert result, {'target': 'something'}


def test_dict_from_readline_with_empty_input():
    value = "\n\r"
    result = engine._dict_from_readline(value)
    assert result == {}


def test_dict_from_readline_with_invalid_input():
    value = "somethinginvalid"
    result = engine._dict_from_readline(value)
    assert result == {}


def test_prepare_command():
    command = "fab production deploy"
    result = engine._prepare_command(command)
    assert result == ['fab', 'production', 'deploy']
