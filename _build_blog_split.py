# -*- coding: utf-8 -*-
"""Split AR blog posts into separate HTML files and trim ar/blog/index.html."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AR_INDEX = ROOT / "ar" / "blog" / "index.html"
TMP1 = ROOT / "_tmp_ar_post1.html"
TMP2 = ROOT / "_tmp_ar_post2.html"

full = AR_INDEX.read_text(encoding="utf-8")
pre_body, after_body = full.split("<body>", 1)
main_header = after_body.split("</header>", 1)[0] + "</header>"
footer = full[full.index("<!-- Footer -->") :]

post1_inner = TMP1.read_text(encoding="utf-8")
post2_inner = TMP2.read_text(encoding="utf-8")
wrap1 = '    <div class="cs-blog-root" id="post-photo-report">\n' + post1_inner.lstrip("\n")
wrap2 = '    <div class="cs-blog-root" id="post-gcc-ai">\n' + post2_inner.lstrip("\n")

back1 = """
    <div class="cs-blog-progress" id="csBlogProgress" aria-label="تقدّم القراءة"></div>
    <nav class="cs-blog-back-bar" aria-label="تنقّل المدونة">
        <div class="container cs-blog-back-bar__inner">
            <a href="index.html" class="cs-blog-back-bar__link">العودة إلى المدونة</a>
            <a href="../../blog/when-photo-becomes-report.html" class="cs-blog-back-bar__link cs-blog-back-bar__link--secondary" hreflang="en">English</a>
        </div>
    </nav>
"""

back2 = """
    <div class="cs-blog-progress" id="csBlogProgress" aria-label="تقدّم القراءة"></div>
    <nav class="cs-blog-back-bar" aria-label="تنقّل المدونة">
        <div class="container cs-blog-back-bar__inner">
            <a href="index.html" class="cs-blog-back-bar__link">العودة إلى المدونة</a>
            <a href="../../blog/gulf-insurers-ai-assessment.html" class="cs-blog-back-bar__link cs-blog-back-bar__link--secondary" hreflang="en">English</a>
        </div>
    </nav>
"""


def patch_lang(header: str, en_href: str) -> str:
    return header.replace(
        '<li><a href="../../blog/index.html">EN</a></li>',
        f'<li><a href="{en_href}" hreflang="en">EN</a></li>',
        1,
    )


def patch_head_title_desc(html_head: str, title: str, desc: str) -> str:
    h = html_head.replace(
        "<title>المدونة | تقييم أضرار السيارات بالذكاء الاصطناعي في الخليج — CarSee</title>",
        f"<title>{title}</title>",
        1,
    )
    h = h.replace(
        'content="كيف تُغيّر تقنية الذكاء الاصطناعي طريقة تقييم أضرار السيارات في دول الخليج؟ مقالات وآخر الأخبار من CarSee."',
        f'content="{desc}"',
        1,
    )
    return h


def strip_inline_blog_script(page: str) -> str:
    return re.sub(
        r"<script>\s*\(function \(\) \{[\s\S]*?\}\)\(\);\s*</script>\s*",
        "",
        page,
        count=1,
    )


def ensure_progress_script(page: str) -> str:
    if "blog-read-progress.js" in page:
        return page
    return page.replace(
        '<script src="../../js/main.js"></script>',
        '<script src="../../js/main.js"></script>\n    <script src="../../js/blog-read-progress.js"></script>',
        1,
    )


head_base = pre_body + "<body>\n"

head1 = patch_head_title_desc(
    pre_body,
    "حين تُصبح الصورة تقريراً | المدونة — CarSee",
    "كيف تتغيّر معادلة توثيق أضرار السيارات من المعاينة اليدوية إلى التقرير الرقمي؟ مقال من مدونة CarSee.",
)
head2 = patch_head_title_desc(
    pre_body,
    "التأمين والذكاء الاصطناعي في الخليج | المدونة — CarSee",
    "لماذا تتحوّل شركات التأمين في الخليج إلى تقييم أضرار السيارات بالذكاء الاصطناعي؟ مقال من مدونة CarSee.",
)

page1 = (
    head1
    + "<body>\n"
    + patch_lang(main_header, "../../blog/when-photo-becomes-report.html")
    + back1
    + wrap1
    + "\n"
    + footer
)
page2 = (
    head2
    + "<body>\n"
    + patch_lang(main_header, "../../blog/gulf-insurers-ai-assessment.html")
    + back2
    + wrap2
    + "\n"
    + footer
)

page1 = ensure_progress_script(strip_inline_blog_script(page1))
page2 = ensure_progress_script(strip_inline_blog_script(page2))

(ROOT / "ar" / "blog" / "when-photo-becomes-report.html").write_text(page1, encoding="utf-8")
(ROOT / "ar" / "blog" / "gulf-insurers-ai-assessment.html").write_text(page2, encoding="utf-8")

# Trim index: pre_body + body + header + hero & rail only; remove progress + articles + inline script
prog = '\n    <div class="cs-blog-progress" id="csBlogProgress" aria-hidden="true"></div>\n'
main_header_idx = main_header.replace(prog, "\n", 1) if prog in main_header else main_header

rail_start = full.index('<section class="hero"')
rail_end = full.index('    <div class="cs-blog-root"')
rail = full[rail_start:rail_end]
rail = rail.replace('href="#post-photo-report"', 'href="when-photo-becomes-report.html"', 1)
rail = rail.replace('href="#post-gcc-ai"', 'href="gulf-insurers-ai-assessment.html"', 1)

footer_idx = strip_inline_blog_script(full[full.index("<!-- Footer -->") :])
new_index = pre_body + "<body>\n" + main_header_idx + "\n\n" + rail + "\n" + footer_idx
AR_INDEX.write_text(new_index, encoding="utf-8")

print("OK: AR article pages + trimmed index")
