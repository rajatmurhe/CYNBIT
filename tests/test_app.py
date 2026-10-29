from streamlit.testing.v1 import AppTest

from cynbit_discovery.engine import ROOT


def button(app, label):
    return next(item for item in app.button if item.label == label)


def test_submit_clear_and_validation():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    assert not app.exception
    button(app, "Prepare discovery brief").click().run()
    assert not app.exception
    assert app.session_state["result"]["suggested_route"] == "ai_automation"
    assert len(app.get("download_button")) == 2
    button(app, "Clear workspace").click().run()
    assert not app.exception
    assert app.text_area[0].value == ""
    button(app, "Prepare discovery brief").click().run()
    assert not app.exception
    assert app.error
    assert len(app.get("download_button")) == 0


def test_unknown_inquiry_and_sample_switch():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    app.text_area[0].set_value("Please suggest a pasta recipe for dinner.")
    button(app, "Prepare discovery brief").click().run()
    assert app.session_state["result"]["status"] == "needs_context"
    app.selectbox[0].select("Manage rental operations").run()
    button(app, "Load sample").click().run()
    assert len(app.get("download_button")) == 0
    button(app, "Prepare discovery brief").click().run()
    assert app.session_state["result"]["suggested_route"] == "tenantease"
    assert not app.exception
