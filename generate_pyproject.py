#!/usr/bin/env python3
"""
현재 가상환경에 설치된 모든 패키지를 pyproject.toml에 추가하는 스크립트
"""

import subprocess
import re
import toml
from pathlib import Path


def get_installed_packages():
    """현재 설치된 패키지 목록을 가져옵니다."""
    try:
        result = subprocess.run(
            ["uv", "pip", "list", "--format=freeze"],
            capture_output=True,
            text=True,
            check=True,
        )
        packages = []
        for line in result.stdout.strip().split("\n"):
            if "==" in line:
                name, version = line.split("==", 1)
                packages.append((name, version))
        return packages
    except subprocess.CalledProcessError as e:
        print(f"패키지 목록을 가져오는 중 오류 발생: {e}")
        return []


def filter_packages(packages):
    """중요한 패키지만 필터링합니다."""
    # 제외할 패키지들 (표준 라이브러리나 불필요한 패키지들)
    exclude_packages = {
        "pip",
        "setuptools",
        "wheel",
        "distlib",
        "filelock",
        "platformdirs",
        "pywin32",
        "pywinpty",
        "sqlite3",
        "asyncio",  # Windows 특화 패키지들
    }

    # 포함할 주요 패키지 카테고리
    include_patterns = [
        "langchain",
        "langgraph",
        "langsmith",
        "openai",
        "anthropic",
        "google",
        "huggingface",
        "jupyter",
        "ipython",
        "notebook",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "streamlit",
        "fastapi",
        "uvicorn",
        "pydantic",
        "pytest",
        "black",
        "isort",
        "chromadb",
        "pinecone",
        "elasticsearch",
        "transformers",
        "torch",
        "sentence-transformers",
        "ragas",
        "rank-bm25",
        "flashrank",
        "kiwipiepy",
        "konlpy",
        "nltk",
        "spacy",
        "pypdf",
        "pymupdf",
        "pdfplumber",
        "beautifulsoup4",
        "lxml",
        "requests",
        "httpx",
        "python-dotenv",
        "pyyaml",
        "jinja2",
        "redis",
        "pymongo",
        "sqlalchemy",
        "celery",
        "prometheus",
        "structlog",
        "onnxruntime",
        "opencv-python",
        "pillow",
        "plotly",
        "altair",
        "scikit-learn",
        "scipy",
    ]

    filtered_packages = []

    for name, version in packages:
        if name.lower() in exclude_packages:
            continue

        # 포함 패턴과 매치되는지 확인
        should_include = any(pattern in name.lower() for pattern in include_patterns)

        if should_include:
            filtered_packages.append((name, version))

    return filtered_packages


def update_pyproject_toml(packages):
    """pyproject.toml 파일을 업데이트합니다."""
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        print("pyproject.toml 파일이 존재하지 않습니다.")
        return

    # 기존 pyproject.toml 읽기
    with open(pyproject_path, "r", encoding="utf-8") as f:
        data = toml.load(f)

    # dependencies 섹션이 없으면 생성
    if "project" not in data:
        data["project"] = {}

    # 패키지들을 dependencies에 추가
    dependencies = []
    for name, version in packages:
        dependencies.append(f"{name}>={version}")

    data["project"]["dependencies"] = dependencies

    # pyproject.toml 업데이트
    with open(pyproject_path, "w", encoding="utf-8") as f:
        toml.dump(data, f)

    print(
        f"pyproject.toml이 업데이트되었습니다. {len(packages)}개의 패키지가 추가되었습니다."
    )


def main():
    print("현재 설치된 패키지 목록을 가져오는 중...")
    packages = get_installed_packages()

    if not packages:
        print("설치된 패키지를 찾을 수 없습니다.")
        return

    print(f"총 {len(packages)}개의 패키지를 발견했습니다.")

    print("패키지 필터링 중...")
    filtered_packages = filter_packages(packages)

    print(f"필터링 후 {len(filtered_packages)}개의 패키지가 선택되었습니다.")

    print("pyproject.toml 업데이트 중...")
    update_pyproject_toml(filtered_packages)

    print("완료되었습니다!")


if __name__ == "__main__":
    main()
