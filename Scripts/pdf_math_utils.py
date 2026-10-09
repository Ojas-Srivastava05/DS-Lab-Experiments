import io
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fpdf import FPDF
from PIL import Image


MATH_DIR = Path(tempfile.gettempdir()) / "ds_lab_math"
MATH_DIR.mkdir(exist_ok=True)
_math_counter = 0


def render_math(latex: str, fontsize: float = 13) -> tuple[str, float, float]:
    """Render LaTeX/mathtext to PNG. Returns path, width_mm, height_mm."""
    global _math_counter
    _math_counter += 1
    path = MATH_DIR / f"eq_{_math_counter}.png"

    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0.0)
    text = fig.text(0, 0, f"${latex}$", fontsize=fontsize)
    fig.canvas.draw()
    bbox = text.get_window_extent(fig.canvas.get_renderer()).transformed(fig.dpi_scale_trans.inverted())
    width_in = max(bbox.width + 0.4, 1.5)
    height_in = max(bbox.height + 0.3, 0.35)

    fig.set_size_inches(width_in, height_in)
    text.set_position((0.05, 0.5))
    text.set_verticalalignment("center")
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.05, transparent=True)
    plt.close(fig)

    with Image.open(path) as img:
        w_px, h_px = img.size
    width_mm = w_px * 25.4 / 200
    height_mm = h_px * 25.4 / 200
    return str(path), width_mm, height_mm


class LabPDF(FPDF):
    def __init__(self, header_text):
        super().__init__()
        self.header_text = header_text
        self._temp_images: list[str] = []

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, self.header_text, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")

    def title_page(self, title, subtitle, meta):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(20, 60, 120)
        self.multi_cell(0, 10, title)
        self.ln(1)
        self.set_font("Helvetica", "B", 13)
        self.multi_cell(0, 8, subtitle)
        self.ln(2)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 5, meta)

    def section_title(self, title):
        self.ln(2)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(20, 60, 120)
        self.multi_cell(0, 7, title)
        self.ln(1)

    def sub_title(self, title):
        self.ln(1)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, title)
        self.ln(0.5)

    def body(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def math(self, latex, fontsize=13):
        path, w_mm, h_mm = render_math(latex, fontsize)
        self._temp_images.append(path)
        usable = self.w - self.l_margin - self.r_margin
        if w_mm > usable:
            scale = usable / w_mm
            w_mm *= scale
            h_mm *= scale
        self.set_x(self.l_margin)
        self.set_fill_color(245, 245, 245)
        self.rect(self.l_margin, self.get_y(), usable, h_mm + 4, style="F")
        self.image(path, x=self.l_margin + 2, y=self.get_y() + 2, w=w_mm, h=h_mm)
        self.ln(h_mm + 6)

    def bullet(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, f"- {text}")

    def table(self, headers, rows, widths):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 10)
        for header, width in zip(headers, widths):
            self.cell(width, 7, header, border=1)
        self.ln()
        self.set_font("Helvetica", "", 10)
        for row in rows:
            self.set_x(self.l_margin)
            for value, width in zip(row, widths):
                self.cell(width, 7, str(value), border=1)
            self.ln()
        self.ln(2)

    def qa_block(self, question, answer):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 10)
        self.multi_cell(0, 5.5, f"Q: {question}")
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, f"A: {answer}")
        self.ln(1)

    def term_block(self, term, definition, latex=None):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(20, 60, 120)
        self.multi_cell(0, 5.5, term)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, definition)
        if latex:
            self.math(latex)
        else:
            self.ln(0.5)


# --- LaTeX formula constants ---

EXP1_FORMULAS = {
    "abs_freq": r"f_i = \text{count of category } i",
    "rel_freq": r"\text{Relative Frequency (\%)} = \frac{f_i}{n} \times 100",
    "cum_freq": r"CF_k = \sum_{i=1}^{k} f_i",
    "prob": r"P(A) = \frac{n(A)}{n}",
    "joint": r"P(A \cap B) = \frac{n(A \cap B)}{n}",
    "marginal": r"P(A) = \frac{n(A)}{n}",
    "conditional": r"P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{n(A \cap B)}{n(B)}",
    "variance": r"\mathrm{Var}(X) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2",
    "std": r"\sigma = \sqrt{\mathrm{Var}(X)}",
    "covariance": r"\mathrm{Cov}(X,Y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})",
    "correlation": r"r = \frac{\mathrm{Cov}(X,Y)}{\sigma_X \,\sigma_Y}",
    "pearson": r"r = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i - \bar{x})^2 \;\sum_{i=1}^{n}(y_i - \bar{y})^2}}",
    "mean_x": r"\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i",
    "mean_y": r"\bar{y} = \frac{1}{n}\sum_{i=1}^{n} y_i",
    "range_r": r"-1 \leq r \leq +1",
}

EXP2_FORMULAS = {
    "mean": r"\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i",
    "variance": r"s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2",
    "std": r"\sigma = \sqrt{s^2}",
    "iqr": r"\mathrm{IQR} = Q_3 - Q_1",
    "lower": r"\text{Lower fence} = Q_1 - 1.5 \times \mathrm{IQR}",
    "upper": r"\text{Upper fence} = Q_3 + 1.5 \times \mathrm{IQR}",
    "missing": r"\text{Missing \%} = \frac{\text{Missing Count}}{\text{Total Rows}} \times 100",
    "covariance": r"\mathrm{Cov}(X,Y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})",
    "correlation": r"r = \frac{\mathrm{Cov}(X,Y)}{\sigma_X \,\sigma_Y}",
}

EXP3_FORMULAS = {
    "zscore": r"z = \frac{x - \mu}{\sigma}",
    "cov_pair": r"\mathrm{Cov}(X,Y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})",
    "cov_matrix": r"\mathbf{C} = \frac{1}{n-1}\mathbf{X}^T\mathbf{X}",
    "eigen": r"\mathbf{C}\mathbf{v} = \lambda \mathbf{v}",
    "transform": r"\mathbf{Z} = \mathbf{X}\mathbf{W}",
    "pc": r"PC_k = \mathbf{X}\mathbf{v}_k",
    "evr": r"\mathrm{EVR}_k = \frac{\lambda_k}{\sum_{i=1}^{p}\lambda_i}",
    "cev": r"\mathrm{CEV}_k = \sum_{i=1}^{k}\mathrm{EVR}_i",
    "ortho": r"PC_i \cdot PC_j = 0 \quad \text{for } i \neq j",
    "variance": r"\mathrm{Var}(X) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2",
}
