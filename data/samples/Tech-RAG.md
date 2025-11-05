---
title: Retrieval-Augmented Generation (RAG) 개념 및 구현
date: 2025-09-05
tags:
  - RAG
  - LLM
  - 검색증강생성
  - AI
  - 딥러닝
keywords: LLM, 외부지식,벡터DB
---

# Retrieval-Augmented Generation (RAG) 개요

## 1. RAG의 필요성

최근 대규모 언어 모델(LLM)은 놀라운 성능을 보여주지만, 학습 시점 이후의 새로운 정보를 반영하지 못하고, 학습 데이터에 없는 내용에 대해 **'Hallucination'** 현상을 보이거나 부정확한 답변을 생성하는 한계가 있습니다. RAG는 이러한 LLM의 한계를 극복하기 위해 외부의 신뢰할 수 있는 지식 소스를 활용하는 방법론입니다.

### 1.1. LLM의 주요 한계
1.  **정보 최신성 부재:** 학습이 완료된 후의 실시간 정보를 알지 못함.
2.  **데이터 소스의 불투명성:** 답변의 근거를 명확히 제시하기 어려움.

## 2. RAG의 작동 원리 (3단계)

RAG는 크게 세 단계로 작동합니다.

### 2.1. 인덱싱 (Indexing)
외부 문서(PDF, Markdown 등)를 작은 청크(Chunk)로 분할하고, 이를 임베딩 모델을 사용해 벡터로 변환합니다. 이 벡터들은 **벡터 데이터베이스(Vector DB)에 저장됩니다.

### 2.2. 검색 (Retrieval)
사용자의 질문(Query)이 들어오면, 이 질문 또한 벡터로 변환됩니다. 벡터 DB에서 질문 벡터와 **가장 유사한(Highest Similarity)** 문서 청크(Context)를 검색합니다.

### 2.3. 생성 (Generation)
검색된 컨텍스트(Source documents)와 원래의 사용자 질문을 하나의 프롬프트로 묶어 LLM에 전달합니다. LLM은 이 **"증강된 프롬프트"를 기반으로 답변을 생성합니다.

```python
# RAG 기본 프롬프트 구성 예시
system_prompt = "다음 Context를 기반으로 User Question에 답변하세요."
user_question = "RAG의 핵심 목적은 무엇인가요?"
retrieved_context = "RAG는 LLM의 환각을 줄이고 최신 정보에 접근하게 합니다."

final_prompt = f"{system_prompt}\n\nContext: {retrieved_context}\n\nQuestion: {user_question}"
# LLM에 final_prompt를 전달하여 답변을 생성합니다.