"""
왼쪽 사이드바 하단에 "노트 업로드", "Vault 경로 입력" 추가해야 함
"""

import os
import streamlit as st

from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="UpThink", page_icon="💭", layout="wide")

st.title("💭 UpThink")
st.caption("지식을 정리하는 사고에만 집중할 수 있음")

# API Key 설정
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")


image_ocr = st.Page(
    "image_ocr.py",
    title="이미지 처리",
    icon=":material/upload_file:",
    default=True,
)
note_summary = st.Page(
    "note_summary.py",
    title="노트 요약",
    icon=":material/summarize:",
)
tag_suggest = st.Page(
    "tag_suggest.py",
    title="태그 추천",
    icon=":material/tag:",
)
related_note = st.Page(
    "related_note.py",
    title="연관 노트 추천",
    icon=":material/note_stack:",
)
note_split = st.Page(
    "note_split.py",
    title="노트 분할",
    icon=":material/split_scene:",
)

pg = st.navigation(
    {
        "노트 정리": [
            image_ocr,
            note_summary,
            tag_suggest,
            related_note,
            note_split,
        ],
    }
)
pg.run()
