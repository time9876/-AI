"""Import smoke tests for the Task 001 project skeleton."""


def test_import_starx_package() -> None:
    import starx

    assert starx


def test_import_core_modules() -> None:
    from starx import hashing, models, serialization

    assert hashing
    assert models
    assert serialization
