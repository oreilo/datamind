from datamind.reports import render_report
def test_pdf():assert render_report("Example",{"value":1},"pdf")[0].startswith(b"%PDF")
def test_docx():assert render_report("Example",{"value":1},"docx")[0].startswith(b"PK")
def test_json():assert b'"value": 1' in render_report("Example",{"value":1},"json")[0]
