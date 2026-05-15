# Future Items & Improvements

이 문서는 Octopith의 향후 개선 사항 및 추가 기능을 기록합니다.

## 1. Search Enhancements
- **Search Mode 설정 기능**: 
    - 사용 목적에 따라 검색 모드를 선택할 수 있는 옵션 제공 (예: `--mode strict`, `--mode broad`).
    - `strict`: 키워드 일치 및 높은 유사도 중심.
    - `broad`: 연관된 맥락 및 광범위한 시맨틱 매칭 중심.

## 2. Intelligence & Summarization
- **Multi-Model 지원**: Ollama 외에도 vLLM, Anthropic/OpenAI API 등 다양한 추론 엔진 연동.
- **Streaming 지원**: 긴 요약 생성 시 실시간으로 결과를 출력하는 스트리밍 기능.

## 3. Operations & Lifecycle
- **대규모 저장소 최적화**: 수백 메가바이트 이상의 SQLite DB 성능 최적화 (Index Tuning).
- **자동 동기화 스케줄러**: 백그라운드에서 주기적으로 저장소를 동기화하는 서비스 모드.
