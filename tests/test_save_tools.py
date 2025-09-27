"""
Unit tests for output/save_tools.py
"""
import os
import tempfile
from output.save_tools import SaveTools

def test_save_and_erase_file():
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf8') as tf:
        temp_path = tf.name

    st = SaveTools(temp_path)
    # Test saving XML
    assert st.save_xml('<test>data</test>\n')
    with open(temp_path, 'r', encoding='utf8') as f:
        content = f.read()
    assert '<test>data</test>' in content

    # Test erasing file
    assert st.erase_file()
    with open(temp_path, 'r', encoding='utf8') as f:
        content = f.read()
    assert content == '\n'

    os.remove(temp_path)

def test_non_existing_file():
    # Should return True for a file that does not exist
    assert SaveTools.non_existing_file('definitely_not_a_real_file_123456789.txt') is True
    # Should return False for a file that exists
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        temp_path = tf.name
    assert SaveTools.non_existing_file(temp_path) is False
    os.remove(temp_path)