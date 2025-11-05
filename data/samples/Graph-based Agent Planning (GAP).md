---
created: 2025-10-31
modified: 2025-10-31
image_processed: False
tags: 
  - upstage-ai-ambassador
  - graph-based-agent-planning
  - ai-agent
  - paper
url:
  - https://arxiv.org/pdf/2510.25320
desc: GAP는 ReAct의 순차적인 병목 현상을 해결하고자 함. 에이전트가 dependency graph를 먼저 그리게 하고, 독립적인 작업을 병렬로 실행하도록 함.
---

![[Graph-based Agent Planning (GAP).png|800]]

1/ GAP란?
GAP(Graph-based Agent Planning)는 ReAct의 순차적인 병목 현상을 해결하기 위해, 에이전트가 dependency graph를 먼저 계획하게 하고 독립적인 작업은 병렬로 실행하도록 훈련시킨 새로운 프레임워크임

2/ 기존 연구의 한계점은?
ReAct와 같은 기존의 패러다임은 sequential reasoning and execution에 의존함
이 때문에 서로 관계가 없는 독립적인 sub-tasks를 병렬로 처리하지 못하고, 한 번에 하나 씩 처리하게 되어 sequential bottleneck이 발생함
Tool의 사용이 비효율적이고 multi-step reasoning에서 성능 저하로 이어지게 됨

3/ 핵심 아이디어는?
에이전트가 복잡한 태스크를 하위 태스크로 분해하고 (task decomposition), 이들 간의 dependency graph를 구성하게 됨
이 그래프를 기반으로 어떤 도구는 병렬로 실행하고 어떤 도구는 순차적으로 돌릴 지 자율적으로 결정함

4/ 아키텍처 및 핵심 방법론 (Architecture & Methodology)

4-1/ Graph-based Task Decomposition
에이전트는 쿼리를 받으면 3가지 작업을 수행함. 서브 태스크 식별(Sub-task Identification), 의존성 분석(Dependency Analysis), 그래프 구성(Graph Construction)
모델은 structured format으로 구조를 출력하게 됨 깔끔하당
```markdown
<graph>
<node id="s1">search("capital of France")</node>
<node id="s2">search("capital of Germany")</node>
<node id="s3" depends="s1">search("population of {s1}")</node>
<node id="s4" depends="s2">search("population of {s2}")</node>
</graph>
```

4-2/ Dependency-Aware Execution Strategies
생성된 graph($G$)는 위상 정렬(topological sorting)을 통해 실행 레벨($L_0, L_1, ..., L_k$)로 분할됨
$L_0$는 의존성이 없는 초기 태스크의 집합
$L_i$는 모든 의존성이 $L_0$ ~ $L_{i-1}$ 레벨에서 충족되는 태스크의 집합
동일한 레벨($L_i$) 내의 모든 태스크는 서로 독립적이므로 병렬로 실행 가능!

5/ Training Pipeline
GAP은 2단계 학습 파이프라인을 사용함. SFT로 기본 전략을 주입하고, RL로 효율성을 최적화함

5-1/ Data Synthesis
NQ, HotpotQA에서 GPT-4o를 사용해 7000개의 고품질 trajectory dataset을 생성함
품질을 높이기 위해 3가지의 필터링 기준을 적용함
	Complexity threshold: 3회 미만의 단순 검색 샘플은 제거
	Task diversity: 병렬 및 순차 검색 비율을 6:4로 유지하여 다양성 확보 (일반화!)
	Length constraint: 약 2000 토큰 초과 샘플은 제거하여 노이즈를 줄임

5-2/ Supervised Fine-tuning for Cold Start
필터링된 데이터셋으로 Qwen2.5-3B-Instruct 모델을 SFT함
이는 모델이 그래프 기반 계획 전략(graph-based planning strategies)을 내재화하는 콜드 스타트 역할을 함

5-3/ End-to-End Agentic Reinforcement Learning
SFT를 통해 얻은 초기 모델을 더욱 정교하게 다듬어, 계산 효율성과 추론 효과성을 최적화하는(optimize computational efficiency or reasoning effectiveness) 단계임
DAPO 및 VeRL  프레임워크를 사용해 RL 기반 파인튜닝을 수행함
보상 함수(reward function)로는 최종 답변이 맞았는지($score_{answer} \in \{0, 1\}$)만 봄

6/ 실험 및 결과
실험 환경: Qwen2.5-3B 모델을 기반으로 7개 QA 벤치마크에서 평가함
평가 지표: 정확도(Exact Match) 및 효율성(Cost-of-Pass)

GAP은 복잡한 Multi-Hop QA 벤치마크에서 SOTA 대비 평균 0.9% 더 높은 정확도를 달성함
HotpotQA: 42.5% (vs AFM-RL 41.1%)
2Wiki: 41.7% (vs AFM-RL 39.8%)

Interaction Turns 감소: 순차적인 방식(Search-R1) 대비 LLM 호출 횟수가 크게 줄어듦
    HotpotQA: 2.27 턴 -> 1.78 턴 (21.6% 감소)
    2Wiki: 3.05 턴 -> 2.03 턴 (33.4% 감소)
Time Cost 단축: HotpotQA에서 248초 -> 168초 (32.3% 감소)
Response Length 감소: HotpotQA에서 554 토큰 -> 416 토큰 (24.9% 감소)
비용 효율성: GAP-3B가 가장 높은 정확도를 달성하면서 동시에 가장 낮은 문제 해결 비용을 보여줌

---

upstage 디코 공유

제목: AI 에이전트의 새로운 일처리 방식, GAP

1/ GAP이 해결하려는 문제는 무엇인가요?

ReAct와 같은 기존의 방식은 AI 에이전트가 복잡한 업무를 처리할 때 한 번에 하나의 행동만 수행한다는 한계를 가지고 있습니다. 이 방법은 순차적인 추론과 실행에 의존하기 때문에, 서로 독립적으로 수행할 수 있는 하위 태스크들이 많음에도 불구하고 동시에 (병렬적으로) 처리하지 못하고 순차적으로 처리되는데요. 결과적으로 전체 완료 시간이 오래 걸리는 순차적 병목 현상(sequential bottleneck)이 발생하게 됩니다.

2/ GAP의 핵심 아이디어는 무엇인가요?

GAP은 이러한 순차적 병목 현상을 해결하기 위해 등장했습니다. 에이전트가 무조건 순서대로 진행하는 것이 아니라, 최적의 실행 순서를 스스로 계획하도록 훈련시킨 것이 핵심입니다.

- 그래프 기반 계획: 에이전트가 요청을 받으면, 우선 필요한 하위 태스크들을 나열합니다. 이 태스크들 사이에 어떤 의존 관계가 있는지 (예: 작업 2가 작업 1의 결과를 반드시 필요로 하는지)를 분석하여 Dependency Graph를 구성합니다.
- 실행 전략 구성: 이 계획을 기반으로, 동시에 처리해도 되는 독립적인 작업들은 한꺼번에 병렬로 실행하고, 이전 작업의 결과가 반드시 필요한 작업들은 순차적으로 진행합니다.

3/ GAP를 사용하여 개선된 점은 무엇인가요?

독립적인 작업들을 병렬로 처리함으로써, AI 에이전트가 작업을 완료하는 데 드는 시간과 자원을 크게 절약할 수 있습니다.

- 더 빠른 실행 속도와 응답성: HotpotQA 데이터셋에서 순차적인 방식의 모델(Search-R1)이 평균 2.27번의 상호작용(interaction turn)이 필요했던 반면, GAP은 1.78번으로 21.6% 감소시켰습니다. 이는 실행 시간 또한 32.3% 단축시키는 결과로 이어졌습니다.
- 짧은 응답 길이와 배포 비용 절감: GAP은 응답 길이(토큰 수)도 24.9% 줄였습니다 (HotpotQA 기준 554 -> 416 토큰). 생성 토큰이 줄면 배포 비용이 줄어들고 처리량(throughput)이 증가하는데, GAP은 가장 높은 정확도를 달성하면서도 'Cost of Pass(문제 해결을 위한 예상 비용)'는 가장 낮춰, 성능과 비용 효율성의 균형을 맞췄습니다.