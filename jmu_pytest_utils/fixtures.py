"""Common test fixtures used in many autograders."""

from pytest import fixture


@fixture
def observable_stdin(monkeypatch, capsys):
    """
    Fixture that replaces builtins.input so prompts are printed
    (capturable by capsys) and test inputs can be fed in.
    """

    def _make_observable_stdin(responses):
        responses_iter = iter(responses)

        def fake_input(prompt=""):
            # mimic real input(): print the prompt
            print(prompt, end="")
            return next(responses_iter)

        monkeypatch.setattr("builtins.input", fake_input)

    return _make_observable_stdin
