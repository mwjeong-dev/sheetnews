#!/usr/bin/env python3
"""연합뉴스 RSS를 내려받아 정적 뷰어의 news.xml을 갱신한다."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


RSS_URL = "https://www.yna.co.kr/rss/news.xml"
OUTPUT_PATH = Path(__file__).with_name("news.xml")
USER_AGENT = "SheetNews/1.0 (local RSS viewer)"


def main() -> None:
    request = Request(RSS_URL, headers={"User-Agent": USER_AGENT})
    temporary_path: Path | None = None

    try:
        with urlopen(request, timeout=20) as response:
            if response.status != 200:
                raise RuntimeError(f"RSS 요청 실패: HTTP {response.status}")
            content = response.read()

        if b"<rss" not in content or b"<item" not in content:
            raise RuntimeError("RSS 형식이 아니거나 기사 항목이 없습니다.")

        with NamedTemporaryFile("wb", dir=OUTPUT_PATH.parent, delete=False) as temporary_file:
            temporary_file.write(content)
            temporary_path = Path(temporary_file.name)
        temporary_path.replace(OUTPUT_PATH)
        print(f"갱신 완료: {OUTPUT_PATH.name} ({content.count(b'<item>')}개 기사)")
    except (HTTPError, URLError, TimeoutError, RuntimeError) as error:
        print(f"갱신 실패: {error}")
        raise SystemExit(1)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


if __name__ == "__main__":
    main()
