"""
Unit tests for forms/form_comparator.py
"""
import os
import tempfile
from forms.form_comparator import compare_forms

def test_compare_forms_equal():
    # Create two identical temporary files
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='ascii') as f1, \
         tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='ascii') as f2:
        f1.write('<root>\n<child>1</child>\n</root>\n')
        f2.write('<root>\n<child>1</child>\n</root>\n')
        f1_path, f2_path = f1.name, f2.name

    results = compare_forms(f1_path, f2_path, max_lines=10)
    assert all(status == 'EQUAL' for _, status, _, _ in results)

    os.remove(f1_path)
    os.remove(f2_path)

def test_compare_forms_non_equal():
    # Create two different temporary files
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='ascii') as f1, \
         tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='ascii') as f2:
        f1.write('<root>\n<child>1</child>\n</root>\n')
        f2.write('<root>\n<child>2</child>\n</root>\n')
        f1_path, f2_path = f1.name, f2.name

    results = compare_forms(f1_path, f2_path, max_lines=10)
    assert any(status == 'NON EQUAL' for _, status, _, _ in results)

    os.remove(f1_path)
    os.remove(f2_path)