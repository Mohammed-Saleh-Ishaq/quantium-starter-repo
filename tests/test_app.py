import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from dash import html, dcc


def find_component(component, component_type, component_id=None):
    if isinstance(component, component_type):
        if component_id is None or component.id == component_id:
            return True

    if hasattr(component, "children"):
        children = component.children
        if isinstance(children, list):
            for child in children:
                if find_component(child, component_type, component_id):
                    return True
        else:
            return find_component(children, component_type, component_id)

    return False


def test_header_is_present():
    layout = app.layout
    assert find_component(layout, html.H1)


def test_visualisation_is_present():
    layout = app.layout
    assert find_component(layout, dcc.Graph, "sales-chart")


def test_region_picker_is_present():
    layout = app.layout
    assert find_component(layout, dcc.RadioItems, "region-radio")
