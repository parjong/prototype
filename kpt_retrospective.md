# Octopith PoC KPT (Keep, Problem, Try) 회고

본 문서는 Octopith PoC 구축 과정을 KPT 프레임워크 기반으로 회고한 문서입니다. 다음 버전의 아키텍처 개선 및 개발 방향을 수립하는 데 목적이 있습니다.

---

## 🟢 Keep (계속 유지할 것 - 잘된 점)

1. **Object-Action 기반 CLI 설계 패턴**
   - `octopith <object> <action>` 구조는 직관적이고 확장성이 뛰어났습니다. 새로운 엔티티(Entity)나 기능이 추가되더라도 일관된 명령어 인터페이스를 유지할 수 있었습니다.
2. **번역을 동반한 영어 요약(Mandatory English Summarization) 전략**
   - 소형 로컬 임베딩 모델(`nomic-embed-text` 등)의 다국어(Multilingual) 한계를 극복하기 위해, **LLM을 통해 문서를 "무조건 영어로 번역 및 요약"하여 임베딩**한 우회 전략은 매우 유효했습니다. 적은 비용과 작은 모델 크기로도 훌륭한 교차 언어(Cross-lingual) 검색 성능을 보여주었습니다.
3. **SQLite + sqlite-vec 기반의 경량 벡터 인프라**
   - 별도의 무거운 Vector DB(Milvus, Pinecone 등)를 띄우지 않고, 로컬 SQLite 생태계 내에서 FTS5(키워드)와 Vector KNN 검색을 단일 파일 DB로 통합 운영한 점은 로컬 애플리케이션인 Octopith의 정체성과 완벽하게 부합했습니다.

---

## 🔴 Problem / Stop (수정 및 중단할 것 - 문제점)

1. **모호한 모델 별칭(Alias)과 타입 혼용 구조**
   - **문제**: DB 스키마(`ModelAlias`)가 요약(Summary) 모델과 임베딩(Embedding) 모델 간에 `"default"`라는 동일한 문자열 별칭을 허용했습니다. 이로 인해 임베딩 작업 시 요약 모델이 호출되어 **차원 불일치(Dimension Mismatch, 2048 != 768)** 크래시가 발생했습니다.
   - **Stop**: 모델을 호출할 때 단순히 `alias` 문자열 하나만으로 조회하는 방식을 중단해야 합니다.
2. **병합 및 필터링 로직의 하드코딩**
   - **문제**: `store.py` 내부에 거리 필터 기준(`distance < 0.3`)과 RRF 스코어링 로직이 하드코딩되어 있었습니다. 검색 결과가 너무 엄격하게 필터링되어 유효한 랭킹 결과가 누락되는 이슈가 있었습니다.
   - **Stop**: 핵심 검색/랭킹 파라미터를 비즈니스 로직(DB 쿼리단)에 하드코딩하는 것을 중단합니다.
3. **병합 시 정렬 누락 등 취약한 Data Pipeline 처리**
   - **문제**: 두 개 이상의 테이블(vec_threads, vec_summaries)에서 온 벡터 검색 결과를 단순히 `.append()`로 이어 붙인 후 RRF 연산으로 넘겨, 요약본 매칭 결과가 하위권으로 밀려나는 치명적인 버그가 있었습니다.

---

## 🔵 Try (새롭게 시도/개선해볼 것 - 다음 버전의 목표)

1. **엄격한 `(Type, Alias)` 복합 구조 도입**
   - 모델 별칭을 관리할 때 반드시 `(model_type, alias)`의 복합 식별자를 사용하도록 모델 관리 스키마와 코드를 전면 개편합니다.
2. **독립적인 `Ranker/Scorer` 모듈 분리**
   - FTS(키워드)와 Vector(의미) 검색 결과를 합치고 점수를 매기는 RRF 로직을 Store 객체에서 분리하여 독립적인 `Scorer` 모듈로 추상화합니다.
   - 이를 통해 BM25 등 다양한 랭킹 알고리즘을 도입하거나, 쿼리 특성에 맞춰 가중치(Weight)를 유연하게 튜닝할 수 있도록 합니다.
3. **동적 임계값 (Dynamic Distance Threshold) 설정**
   - 임베딩 모델(Nomic, Mxbai 등)마다 거리 분포가 다르므로, 모델 스키마에 `default_distance_threshold` 메타데이터를 추가하거나 Config에서 불러와 쿼리 시 유연하게 필터링을 조절할 수 있게 구현합니다.
4. **비동기 처리량 극대화 (Batch Processing)**
   - 다이제스트(Digest) 작업 수행 시 다량의 문서 요약 및 임베딩을 순차 처리하고 있습니다. `asyncio.gather` 및 Chunk 단위의 배치 처리를 도입하여 LLM/Ollama API 병목을 최소화하고 색인 속도를 비약적으로 향상시켜 봅니다.
