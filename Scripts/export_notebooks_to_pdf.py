"""Export experiment notebooks to PDF with outputs via HTML + Chrome."""

from pathlib import Path
import json
import subprocess
import sys

import nbformat
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent.parent
EXPERIMENTS = [
    "Experiment1", "Experiment2", "Experiment3", "Experiment4",
    "Experiment5", "Experiment6", "Experiment7", "Experiment8",
    "Experiment9", "Experiment10",
]
STUDENT_NAME = "Ojas Srivastava"
ROLL_NO = "U24AI028"

COVER_JS = """
([name, roll, title]) => {
    const cover = document.createElement("div");
    cover.style.cssText = "height:230mm;display:flex;flex-direction:column;justify-content:center;"
        + "align-items:center;text-align:center;page-break-after:always;break-after:page;"
        + "font-family:Helvetica,Arial,sans-serif;";
    cover.innerHTML = `<div style="font-size:40px;font-weight:700;margin-bottom:18px">${name}</div>`
        + `<div style="font-size:30px;font-weight:600;margin-bottom:40px">${roll}</div>`
        + `<div style="font-size:20px;color:#555">${title}</div>`;
    document.body.prepend(cover);
}
"""


def repair_notebook(path: Path) -> None:
    nb = json.loads(path.read_text())
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        ec = cell.get("execution_count")
        for out in cell.get("outputs", []):
            otype = out.get("output_type")
            if otype == "stream" and "name" not in out:
                out["name"] = "stdout"
            elif otype == "execute_result":
                out.setdefault("metadata", {})
                out.setdefault("execution_count", ec)
            elif otype == "display_data":
                out.setdefault("metadata", {})
        if "id" not in cell:
            cell["id"] = f"cell-{abs(hash(str(cell.get('source'))) % 10**8)}"
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    nbformat.validate(nbformat.read(path, as_version=4))


def export_html(notebook: Path, html_out: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "html",
            str(notebook),
            "--output",
            html_out.stem,
            "--output-dir",
            str(html_out.parent),
        ],
        check=True,
        cwd=str(BASE),
    )


def html_to_pdf(html_path: Path, pdf_path: Path, title: str = "") -> None:
    url = html_path.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.evaluate(COVER_JS, [STUDENT_NAME, ROLL_NO, title])
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "12mm", "bottom": "12mm", "left": "10mm", "right": "10mm"},
        )
        browser.close()


def main():
    for exp in EXPERIMENTS:
        nb = BASE / exp / "Notebook.ipynb"
        if not nb.exists():
            print(f"Skip missing: {nb}")
            continue

        html_path = BASE / exp / "Notebook_with_outputs.html"
        pdf_path = BASE / exp / f"{ROLL_NO}_{exp}_Output.pdf"
        (BASE / exp / "Notebook_with_outputs.pdf").unlink(missing_ok=True)

        print(f"Exporting HTML: {exp}")
        repair_notebook(nb)
        export_html(nb, html_path)

        print(f"Converting PDF: {exp}")
        html_to_pdf(html_path, pdf_path, exp.replace("Experiment", "Experiment "))
        print(f"Created: {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")

        html_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
