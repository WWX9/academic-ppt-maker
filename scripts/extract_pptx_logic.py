from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

TITLE_TYPES = {"title", "ctrTitle"}


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def text_from_shape(shape: ET.Element) -> str:
    parts = []
    for node in shape.findall(".//a:t", NS):
        if node.text:
            parts.append(node.text)
    return normalize_text(" ".join(parts))


def shape_is_title(shape: ET.Element) -> bool:
    ph = shape.find("./p:nvSpPr/p:nvPr/p:ph", NS)
    if ph is None:
        return False
    return ph.get("type", "title") in TITLE_TYPES


def load_xml(zf: zipfile.ZipFile, name: str) -> ET.Element:
    return ET.fromstring(zf.read(name))


def slide_order(zf: zipfile.ZipFile) -> list[str]:
    presentation = load_xml(zf, "ppt/presentation.xml")
    rels = load_xml(zf, "ppt/_rels/presentation.xml.rels")
    rel_map = {
        rel.get("Id"): rel.get("Target")
        for rel in rels.findall("./rel:Relationship", NS)
    }
    ordered = []
    for slide_id in presentation.findall("./p:sldIdLst/p:sldId", NS):
        rel_id = slide_id.get(f"{{{NS['r']}}}id")
        target = rel_map.get(rel_id)
        if not target:
            continue
        ordered.append("ppt/" + target.lstrip("/").replace("\\", "/"))
    return ordered


def extract_slide(slide_xml: ET.Element) -> dict:
    texts = []
    title = ""
    for shape in slide_xml.findall(".//p:sp", NS):
        text = text_from_shape(shape)
        if not text:
            continue
        texts.append(text)
        if not title and shape_is_title(shape):
            title = text

    if not title and texts:
        title = texts[0]

    preview = []
    for item in texts:
        if item == title:
            continue
        preview.append(item)
        if len(preview) >= 3:
            break

    return {
        "title": title,
        "text_blocks": len(texts),
        "text_chars": sum(len(item) for item in texts),
        "pictures": len(slide_xml.findall(".//p:pic", NS)),
        "preview": preview,
    }


def outline_signals(slides: list[dict]) -> dict:
    titles = [slide["title"] for slide in slides if slide["title"]]
    joined = " ".join(titles)
    keyword_groups = {
        "background": ["背景", "研究背景", "引言", "问题提出", "motivation", "introduction"],
        "literature": ["文献", "相关工作", "研究现状", "review"],
        "data": ["数据", "研究区", "study area", "dataset"],
        "method": ["方法", "模型", "框架", "method", "framework"],
        "experiment": ["实验", "设置", "experiment"],
        "result": ["结果", "分析", "验证", "results", "analysis"],
        "conclusion": ["结论", "总结", "展望", "future work", "conclusion"],
    }
    hits = {
        name: any(keyword.lower() in joined.lower() for keyword in keywords)
        for name, keywords in keyword_groups.items()
    }
    return {
        "title_coverage": len(titles) / max(len(slides), 1),
        "avg_text_chars_per_slide": round(
            sum(slide["text_chars"] for slide in slides) / max(len(slides), 1), 1
        ),
        "avg_pictures_per_slide": round(
            sum(slide["pictures"] for slide in slides) / max(len(slides), 1), 2
        ),
        "logic_markers": hits,
    }


def analyze_deck(path: Path) -> dict:
    with zipfile.ZipFile(path) as zf:
        ordered = slide_order(zf)
        slides = []
        for name in ordered:
            try:
                slide_xml = load_xml(zf, name)
                slides.append(extract_slide(slide_xml))
            except KeyError:
                continue
    return {
        "file": str(path),
        "name": path.name,
        "size_mb": round(path.stat().st_size / 1024 / 1024, 1),
        "slide_count": len(slides),
        "signals": outline_signals(slides),
        "slides": [
            {
                "index": idx + 1,
                "title": slide["title"],
                "preview": slide["preview"],
                "text_blocks": slide["text_blocks"],
                "text_chars": slide["text_chars"],
                "pictures": slide["pictures"],
            }
            for idx, slide in enumerate(slides)
        ],
    }


def select_candidates(records: list[dict], limit: int) -> list[dict]:
    filtered = []
    for record in records:
        name = record["file"]
        if "1122 厦门" in name:
            continue
        if record["slide_count"] < 8:
            continue
        filtered.append(record)

    def score(record: dict) -> tuple:
        markers = record["signals"]["logic_markers"]
        marker_score = sum(1 for value in markers.values() if value)
        return (
            marker_score,
            record["signals"]["title_coverage"],
            -abs(record["signals"]["avg_text_chars_per_slide"] - 180),
            record["slide_count"],
            -record["size_mb"],
        )

    filtered.sort(key=score, reverse=True)

    chosen = []
    seen_dirs = Counter()
    for record in filtered:
        parent = str(Path(record["file"]).parent)
        if seen_dirs[parent] >= 2:
            continue
        chosen.append(record)
        seen_dirs[parent] += 1
        if len(chosen) >= limit:
            break
    return chosen


def write_markdown(records: list[dict], output: Path) -> None:
    lines = ["# PPT Logic Review Pack", ""]
    for record in records:
        lines.append(f"## {record['name']}")
        lines.append(f"- File: `{record['file']}`")
        lines.append(f"- Slides: {record['slide_count']}")
        lines.append(f"- Size: {record['size_mb']} MB")
        lines.append(
            "- Signals: "
            + json.dumps(record["signals"], ensure_ascii=False, sort_keys=True)
        )
        lines.append("- Outline:")
        for slide in record["slides"][:20]:
            preview = " | ".join(slide["preview"][:2])
            if preview:
                lines.append(
                    f"  - {slide['index']:02d}. {slide['title'] or '[Untitled]'} :: {preview}"
                )
            else:
                lines.append(f"  - {slide['index']:02d}. {slide['title'] or '[Untitled]'}")
        if len(record["slides"]) > 20:
            lines.append(f"  - ... ({len(record['slides']) - 20} more slides)")
        lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--md-output", type=Path, required=True)
    args = parser.parse_args()

    files = sorted(args.root.rglob("*.pptx"))
    records = []
    for path in files:
        try:
            records.append(analyze_deck(path))
        except zipfile.BadZipFile:
            continue

    selected = select_candidates(records, args.limit)
    args.json_output.write_text(
        json.dumps(selected, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(selected, args.md_output)
    print(f"analyzed={len(records)} selected={len(selected)}")


if __name__ == "__main__":
    main()
