from tvsummary.main import main


# Test that a missing configuration returns exit code 1.
def test_main_missing_config(tmp_path, capsys):
    # Use a configuration path that does not exist.
    missing_config = tmp_path / "missing.toml"

    # Run the application with the invalid configuration path.
    exit_code = main(["--config", str(missing_config)])

    # Capture the application's terminal output.
    captured = capsys.readouterr()

    # Check the failure exit code and error message.
    assert exit_code == 1
    assert "Error:" in captured.err
    assert "Could not load configuration" in captured.err
    assert "Traceback" not in captured.err
